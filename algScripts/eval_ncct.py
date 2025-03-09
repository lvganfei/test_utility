#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import glob
import json
import datetime
import traceback

import pydicom
import argparse
import numpy as np
import pandas as pd
import SimpleITK as sitk
import matplotlib.pyplot as plt

from collections import Counter
from tqdm import tqdm
from pathlib import Path
from skimage.measure import label, regionprops
from scipy.ndimage import zoom
from collections import defaultdict, OrderedDict
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report


LABEL_DICT = {
    1: 'CPH',
    2: 'IH',
    3: 'SH',
    4: 'EH',
    5: 'SAH'
}

# DICE阈值
DICE_THRESH = 0
# 日志文件名，pipeline跑应改为ncct.log
LOG_FILE = 'ncct.log'

parser = argparse.ArgumentParser('NCCT evaluation')
parser.add_argument('-O', '--output',  type=str,
                    default='/data/NCCT/')
parser.add_argument('-A', '--answer',  type=str,
                    default='/workspace/data/NCCT/ncct_test_ans')
parser.add_argument('-M', '--mapping', type=str,
                    default='/workspace/data/NCCT/mapping.csv')
parser.add_argument('--debug', type=bool, default=False)
args = parser.parse_args()

DEBUG_MODE = args.debug


def get_status(log_stream):
    res = re.findall('Alg version: (.*)\n', log_stream, re.I)
    ver = ''
    if len(res) > 0:
        ver = res[0]
    res = re.findall('All Completed in (.*) !!!', log_stream, re.I)
    tol_time = ''
    if len(res) > 0:
        tol_time = res[0]
    return ver, tol_time


def cal_dice(target, pred):
    num = np.sum(target * pred)
    den = np.sum(target) + np.sum(pred)
    smooth = 1e-6
    dice = (2 * num) / (den + smooth)
    dice = round(dice, 4)
    return dice


def get_metric(target_mask, pred_mask, overview):
    ll_t = label(target_mask > 0)
    # 体积<20像素不认为是阳性，不纳入计算
    props_t = [p for p in regionprops(ll_t) if p.area >= 20]
    fns = [p.label for p in props_t]
    fps = list(range(1, pred_mask.max()+1))
    tps = []
    rows = []

    # 1. 找出正确的预测区域，真阳
    for prop_t in props_t:
        region_t = ll_t == prop_t.label
        z, y, x = np.where(region_t)
        n_max_z0 = Counter(z).most_common()[0][0]
        loc_t = np.rint(prop_t.centroid).astype(int).tolist()
        lb_t = np.unique(target_mask[region_t]).astype(int)
        lb_t = [LABEL_DICT[i] for i in lb_t if i in LABEL_DICT.keys()]

        is_tp = False
        for lb_p in range(1, pred_mask.max()+1):
            region_p = pred_mask == lb_p
            region_p_info = overview['segments_all'][lb_p - 1]

            area = region_p.sum()
            # <20的预测区域去掉，不纳入计算
            if area < 20:
                if lb_p in fps:
                    fps.remove(lb_p)
                continue

            zz, yy, xx = np.where(region_p)
            n_max_z1 = Counter(zz).most_common()[0][0]
            loc_p = np.rint(np.asarray([zz, yy, xx]).mean(1)).astype(int).tolist()

            dice = cal_dice(region_t, region_p)
            if dice > DICE_THRESH:
                is_tp = True
                rows.append([
                    loc_t, n_max_z0, prop_t.area, lb_t,  # TARGET
                    loc_p, n_max_z1, area, region_p_info['type'], region_p_info['clstype'],  # PRED
                    dice, 'TP'
                ])
                if prop_t.label not in tps:
                    tps.append(prop_t.label)
                if prop_t.label in fns:
                    fns.remove(prop_t.label)
                if lb_p in fps:
                    fps.remove(lb_p)

        # 该region没有被预测出来，假阴
        if not is_tp:
            rows.append([
                loc_t, n_max_z0, prop_t.area, lb_t,
                'NULL', 'NULL', 'NULL', 'NULL', 'NULL',
                0, 'FN'
            ])

    # 2. 余下的都是假阳
    for lb_p in fps:
        region_p = pred_mask == lb_p
        region_p_info = overview['segments_all'][lb_p - 1]

        area = region_p.sum()
        zz, yy, xx = np.where(region_p)
        n_max_z1 = Counter(zz).most_common()[0][0]
        loc_p = np.rint(np.asarray([zz, yy, xx]).mean(1)).astype(int).tolist()

        rows.append([
            'NULL', 'NULL', 'NULL', 'NULL',
            loc_p, n_max_z1, area, region_p_info['type'], region_p_info['clstype'],
            0, 'FP'
        ])

    # 3. 真阴case并且预测也是真阴
    if len(rows) < 1:
        rows.append([
            'NULL', 'NULL', 'NULL', 'NULL',
            'NULL', 'NULL', 'NULL', 'NULL', 'NULL',
            'NULL', 'TN'
        ])

    # 拆开答案类别中多个答案的
    new_rows = []
    lenth = len(rows)
    for i in range(lenth):
        if type(rows[i][3]) == list and len(rows[i][3]) > 1:
            modelrow = rows[i]
            print(modelrow[3])
            cls_ans = modelrow[3]
            
            for j in range(len(cls_ans)):
                temprow = modelrow
                temprow[3] = cls_ans[j]
                new_rows.append(temprow)
        elif type(rows[i][3]) == list and len(rows[i][3]) == 1:
            rows[i][3] = ''.join(rows[i][3])
            new_rows.append(rows[i])
        else:
            print('weird str')
            new_rows.append(rows[i])
    # 4. 组合信息
    df = pd.DataFrame(data=new_rows, columns=[
        '答案位置', '答案最大层面', '答案体积', '答案类别',
        '预测位置', '预测最大层面', '预测体积', '预测类别', '分类类别',
        'DICE', '类型'
    ])
    return df


def single_case(case_dir, case_answer_dir):
    dcms = list((case_dir/'slices').glob('*.dcm'))
    if len(dcms) < 1:
        if DEBUG_MODE: print(case_dir.name, 'no dcm files')
        return None

    dcm = pydicom.read_file(str(dcms[0]))
    p_name = str(dcm.PatientName)
    p_id = dcm.PatientID

    target_mask = case_answer_dir/'anno.nii.gz'
    pred_mask = case_dir/'mask.npy'
    overview_json = case_dir/'overview.json'
    log_file = case_dir/LOG_FILE

    # 以下文件如果不存在则返回空
    if not target_mask.exists():
        target_mask = case_answer_dir/'anno.nii'
        if not target_mask.exists():
            if DEBUG_MODE: print(case_dir.name, p_name, 'no target_mask')
            return None
    elif not pred_mask.exists():
        if DEBUG_MODE: print(case_dir.name, p_name, 'no pred_mask')
        return None
    elif not overview_json.exists():
        if DEBUG_MODE: print(case_dir.name, p_name, 'no overview.json')
        return None
    if not log_file.exists():
        log_file = case_dir/'_test.'.join(LOG_FILE.split('.'))
        if not log_file.exists():
            if DEBUG_MODE: print(case_dir.name, p_name, 'no ncct log')
            return None

    # 读取版本号、用时、记录等信息
    with open(log_file, 'r', encoding='utf8') as lf:
        ver, tol_time = get_status(lf.read())
    with open(overview_json, 'r', encoding='utf8') as oj:
        overview = json.load(oj)

    # 加载target_mask pred_mask
    target_mask = sitk.GetArrayFromImage(sitk.ReadImage(str(target_mask)))
    pred_mask = np.load(pred_mask)
    target_mask = zoom(target_mask, np.array(pred_mask.shape)/target_mask.shape, order=0)[::-1]

    # 计算指标
    single_df = get_metric(target_mask, pred_mask, overview)

    # 添加额外信息
    single_df['folder_name'] = case_dir.name
    single_df['answer_name'] = case_answer_dir.name
    single_df['patient_name'] = p_name
    single_df['patient_id'] = p_id
    single_df['time'] = tol_time
    single_df['version'] = ver

    return single_df


def main():
    output_dir  = Path(args.output)
    answer_dir  = Path(args.answer)
    mapping_dir = Path(args.mapping)

    info = pd.read_csv(mapping_dir)
    info = info.apply(lambda x: x.apply(lambda y: re.sub(r'\t\r\n', '', y).strip()))
    info = info.apply(lambda x: [x['image'], x['anno']], axis=1)

    dfs = []
    for case_dir_name, case_answer_dir_name in tqdm(info):
        try:
            res = single_case(output_dir/case_dir_name, answer_dir/case_answer_dir_name)
            if res is not None: dfs.append(res)
        except Exception as e:
            print(case_dir_name, e)
            traceback.print_exc()
            exit(1)
    if len(dfs) > 0:
        df = pd.concat(dfs)
        now_time = datetime.datetime.now()
        save_path = answer_dir.parent/'ncct_eval_{}{:02d}{:02d}-{:02d}{:02d}.csv'.format(
            now_time.year,
            now_time.month,
            now_time.day,
            now_time.hour,
            now_time.minute
        )
        df = df[[
            'folder_name', 'answer_name', 'patient_name', 'patient_id',
            '答案位置', '预测位置', '答案最大层面', '预测最大层面', '答案体积', '预测体积', '答案类别', '预测类别', '分类类别',
            'DICE', '类型', 'time', 'version'
        ]]
        df.to_csv(save_path, index=False)

        # 计算每个case的平均指标
        res = defaultdict(list)
        for case in df.groupby('patient_name'):
            patient_name, info = case
            tps, fns, fps, tns = [info[info['类型'] == x] for x in ['TP', 'FN', 'FP', 'TN']]

            # 计算分割的指标
            precision = len(tps) / (len(tps) + len(fps) + 1e-6)
            recall = len(tps) / (len(tps) + len(fns) + 1e-6)
            res['patient_name'].append(patient_name)
            res['seg_precision'].append('NULL' if len(tns) > 0 else precision)
            res['seg_recall'].append('NULL' if len(tns) > 0 else recall)

            # 计算加上规则的分类指标
            mixtps = tps[tps.apply(lambda x: x['预测类别'] in x['答案类别'], axis=1)]
            accuracy = len(mixtps) / (len(tps) + 1e-6)
            res['mix_accuracy'].append(accuracy if len(tps) > 0 else 'NULL')

            # 计算纯分类模型的分类指标
            clstps = tps[tps.apply(lambda x: x['分类类别'] in x['答案类别'], axis=1)]
            accuracy = len(clstps) / (len(tps) + 1e-6)
            res['cls_accuracy'].append(accuracy if len(tps) > 0 else 'NULL')

        # 计算所有case的平均指标
        avg_seg_precision = np.mean([x for x in res['seg_precision'] if x != 'NULL'])
        avg_seg_recall    = np.mean([x for x in res['seg_recall']    if x != 'NULL'])
        avg_mix_accuracy  = np.mean([x for x in res['mix_accuracy']  if x != 'NULL'])
        avg_cls_accuracy  = np.mean([x for x in res['cls_accuracy']  if x != 'NULL'])

        # 所有case的平均指标加入到df里
        res['patient_name'].append('AVERAGE')
        res['seg_precision'].append(avg_seg_precision)
        res['seg_recall'].append(avg_seg_recall)
        res['mix_accuracy'].append(avg_mix_accuracy)
        res['cls_accuracy'].append(avg_cls_accuracy)

        # 生成csv
        res = pd.DataFrame(res)
        res.to_csv(save_path.parent/f'{save_path.stem}_prc.csv')

        # 计算混淆矩阵
        
        ans_cls = df['答案类别'].values.tolist()
        print(ans_cls)
        print(len(ans_cls))
        predict_cls = df['预测类别'].values.tolist()
        print(predict_cls)
        print(len(predict_cls))

        cm = df[df['类型'] == 'TP']
        tp_ans_cls = cm['答案类别'].values.tolist()
        tp_predict_cls = cm['预测类别'].values.tolist()
        overall_report = classification_report(ans_cls, predict_cls)
        tp_report = classification_report(tp_ans_cls, tp_predict_cls)
        print('------------overall_report------------')
        print(overall_report)
        print('------------tp_report------------')
        print(tp_report)
        # key_map = OrderedDict([('CPH', 0), ('IH', 1), ('SH', 2), ('EH', 3), ('SAH', 4)])
        # yf = lambda x: x['预测类别'] if x['预测类别'] in x['答案类别'] else x['答案类别'][0]
        # y = cm.apply(yf, axis=1).apply(lambda x: key_map[x]).apply(int)
        # p = cm['预测类别'].apply(lambda x: key_map[x]).apply(int)
        # confmat = confusion_matrix(y, p)
        # disp = ConfusionMatrixDisplay(confmat, display_labels=key_map.keys()).plot()
        # disp.figure_.savefig(save_path.parent/f'{save_path.stem}_cm.png')
    else:
        print('no result')


if __name__ == '__main__':
    main()

# python3 -u /home/devops1/NCCT/eval_ncct.py -O /data1/ruijin/data/output/strokedoc -A /home/devops1/NCCT/ncct_test_ans/ncct_test_ans -M /home/devops1/NCCT/mapping.csv
# sudo nvidia-docker run -it --rm -e NVIDIA_VISIBLE_DEVICES=1 -v "/data1/ruijin/data/source/strokedoc:/workspace" -v "/data1/ruijin/data/output/strokedoc:/output" harbor.democompany.net:5050/alg/stroke/cerebral_ncct:2.0.0.d04299c1.cuda11
