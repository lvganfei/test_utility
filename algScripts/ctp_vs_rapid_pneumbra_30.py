# -*- coding: utf-8 -*-
import pymongo
import numpy as np
import csv
import time
import pymysql
import sys
import json
import pandas as pd 
import os
from scipy import stats


#env = "105_production"
#myclient = pymongo.MongoClient("mongodb://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@10.10.10.105:17017/plt_ctpdoc")

# 连接数据库
# db_connect = pymysql.Connect(
#     host='10.10.10.105',
#     port=13306,
#     user='root',
#     passwd='qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj',
#     db='plt_ctpdoc',
#     charset='utf8'
# )

#


args=sys.argv
host = args[1]
rapid_path = args[2]
version = args[3]


env = "ruijin"
myclient = pymongo.MongoClient("mongodb://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@" + host + ":14209/plt_ctpdoc")
env_mysql = "ruijin"
#打开数据库连接
#连接数据库
db_connect = pymysql.Connect(
    host=host,
    port=20158,
    user='root',
    passwd='qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj',
    db='plt_ctpdoc',
    charset='utf8'
)


db = myclient.plt_ctpdoc
metas = db['metas']


def check_case_exist(db, case_num):
    # 使用cursor()方法获取操作游标
    is_exist = False
    cursor = db.cursor()

    # SQL 查询语句
    sql = f"SELECT * FROM plt_ctpdoc.cases where case_num ='{case_num}';"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # print(cursor.rownumber)
        result = cursor.fetchone()
        if result != None:
            # print(result, cursor.rownumber)
            is_exist = True
    except:
        print("Error: unable to fetch data")
    return is_exist


def find_max(list):
    max = list[0][1]
    max_index = 0
    for i in range(len(list)):
        if max < list[i][1]:
            max = list[i][1]
            max_index = i
    return max, max_index

def deffuse(core, penumbra):
    ratio = float('inf') if core == 0 else penumbra/core

    if (core < 70 and ratio > 1.8 and (penumbra - core) > 15):
        return "Y"
    return "N"

def extend(core, penumbra):
    ratio = float('inf') if core == 0 else penumbra/core

    if (core < 70 and ratio > 1.2 and (penumbra - core) > 10):
        return "Y"
    return "N"

def volume_compare(rapid_v, sk_v):
    if rapid_v == 0:
        if abs(rapid_v - sk_v) <= 10:
            return "Y"
        return "N"
    else:
        if (abs(rapid_v - sk_v)/rapid_v <= 0.2 or abs(rapid_v - sk_v) <= 10):
            return "Y"
        return "N"

def volume_compare_penumbra(rapid_v, sk_v):
    if rapid_v == 0:
        if abs(rapid_v - sk_v) <= 10:
            return "Y"
        return "N"
    else:
        if (abs(rapid_v - sk_v)/rapid_v <= 0.3 or abs(rapid_v - sk_v) <= 10):
            return "Y"
        return "N"



ignore_cases = []
# ignore_cases = ['0001744805', '0007400446', '0008248086', '0007411236', '0009095934', 'K00192706', '0009084169']

with open(rapid_path) as rapid_answer:
    rapid_mismatches = json.load(rapid_answer)
    print(rapid_mismatches)

variance_core = []
variance_penumbra = []
variance_tdc_artery_peak = []
variance_tdc_artery_time = []
variance_tdc_vein_peak = []
variance_tdc_vein_time = []
items = []
rapid_core_arr = []
sk_core_arr = []
rapid_penumbra_arr = []
sk_penumbra_arr = []

items.append(
    ["patient_id", "patient_name", "core", "rapid_core", "penumbra", "rapid_penumbra", "tdc_artery_peak",
     "rapid_tdc_artery_peak",
     "tdc_artery_time", "rapid_tdc_artery_time", "tdc_vein_peak", "rapid_tdc_vein_peak", "tdc_vein_time",
     "rapid_tdc_vein_time", "mishmatch_volume", "mismatch_ratio",  "rapid_mishmatch_volume", "rapid_mismatch_ratio","defuse_sk","defuse_rapid","extend_sk","extend_rapid","core_compare_result","penumbra_compare_result","defuse_match","extend_match"])
for rapid_mismatch in rapid_mismatches:
    item = []
    patient_id = rapid_mismatch.get('patient_id')
    print(patient_id)
    if patient_id in ignore_cases:
        continue
    # case_doc = metas.find_one({"dicom_meta.patient_num": patient_id})
    case_doc = None
    case_doc_list = metas.find({"dicom_meta.patient_num": patient_id})
    for x in case_doc_list:
        if not x.get('overview'):
            continue

        # 判断 数据库中是否存在
        if not check_case_exist(db_connect, x.get('case_num')):
            continue

        case_doc = x
        break

    if case_doc is None:
        print('can not find meta of ' + str(patient_id) + 's\n')
        continue

    core = case_doc['overview']['whole']['core']['volume']
    penumbra = case_doc['overview']['whole']['penumbra']['volume']
    tdc_artery_peak, tdc_artery_time = find_max(case_doc['tdc']['artery']['inter'])
    tdc_vein_peak, tdc_vein_time = find_max(case_doc['tdc']['vein']['inter'])

    rapid_core = rapid_mismatch.get('core')
    rapid_penumbra = rapid_mismatch.get('penumbra')
    rapid_tdc_artery_peak = rapid_mismatch.get("tdc_artery_peak")
    rapid_tdc_artery_time = rapid_mismatch.get("tdc_artery_time")
    rapid_tdc_vein_peak = rapid_mismatch.get("tdc_vein_peak")
    rapid_tdc_vein_time = rapid_mismatch.get("tdc_vein_time")

    rapid_core_arr.append(rapid_core)
    sk_core_arr.append(core)
    rapid_penumbra_arr.append(rapid_penumbra)
    sk_penumbra_arr.append(penumbra)

    item.append(patient_id)
    item.append(case_doc['dicom_meta']['patient_name'])
    item.append(core)
    item.append(rapid_core)

    item.append(penumbra)
    item.append(rapid_penumbra)

    item.append(tdc_artery_peak)
    item.append(rapid_tdc_artery_peak)

    item.append(tdc_artery_time)
    item.append(rapid_tdc_artery_time)

    item.append(tdc_vein_peak)
    item.append(rapid_tdc_vein_peak)

    item.append(tdc_vein_time)
    item.append(rapid_tdc_vein_time)
    item.append(penumbra-core)

    # 输出rapid和数坤取栓溶栓指南

    if core == 0.0:
        item.append("INF")
    else:
        item.append(penumbra/core)
        
        
    item.append(rapid_penumbra-rapid_core)
    if rapid_core == 0.0:
        item.append("INF")
    else:
        item.append(rapid_penumbra/rapid_core)

    sk_extend = extend(core, penumbra)
    sk_deffues = deffuse(core, penumbra)
    rapid_deffuse = deffuse(rapid_core, rapid_penumbra)
    rapid_extend = extend(rapid_core, rapid_penumbra)

    

    # 输出rapid和sk的core差值和百分比是否满足标准
    
    core_volume_compare_result = volume_compare(rapid_core,core)
    
    # 输出rapid和sk的penumbra差值和百分比是否满足标准 30%
    
    penumbra_volume_compare_result = volume_compare_penumbra(rapid_penumbra,penumbra)
    
    defuse_match = "Y" if sk_deffues == rapid_deffuse else "N"
    
    extend_match = "Y" if sk_extend == rapid_extend else "N"
    
    item.extend([sk_deffues,rapid_deffuse,sk_extend,rapid_extend,core_volume_compare_result,penumbra_volume_compare_result,defuse_match,extend_match])

    
    


    variance_core.append(abs(rapid_core - core))
    variance_penumbra.append(abs(rapid_penumbra - penumbra))
    variance_tdc_artery_peak.append(abs(tdc_artery_peak - rapid_tdc_artery_peak))
    variance_tdc_artery_time.append(abs(tdc_artery_time - rapid_tdc_artery_time))
    variance_tdc_vein_peak.append(abs(tdc_artery_peak - rapid_tdc_vein_peak))
    variance_tdc_vein_time.append(abs(tdc_artery_time - rapid_tdc_vein_time))

    items.append(item)

# 关闭数据库连接
db_connect.close()

items.append([])
items.append(["variance_core", "variance_penumbra", "variance_tdc_artery_peak", "variance_tdc_artery_time",
              "variance_tdc_vein_peak", "variance_tdc_vein_time"])
items.append([np.std(variance_core), np.std(variance_penumbra), np.std(variance_tdc_artery_peak),
              np.std(variance_tdc_artery_time), np.std(variance_tdc_vein_peak), np.std(variance_tdc_vein_time)])

core_pearson_cor = stats.pearsonr(rapid_core_arr, sk_core_arr)
print(core_pearson_cor)
penumbra_pearson_cor = stats.pearsonr(rapid_penumbra_arr,sk_penumbra_arr)
print(penumbra_pearson_cor)
items.append(["core_pearson_cor", core_pearson_cor[0],"core_pearson_cor_p",core_pearson_cor[1]])
items.append(["penumbra_pearson_cor", penumbra_pearson_cor[0],"penumbra_pearson_cor",penumbra_pearson_cor[1]])
with open("sk_rapid_compare_pneumbra_" + version + "_new_penumbra_pearsons_" + host + ".csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(items)
