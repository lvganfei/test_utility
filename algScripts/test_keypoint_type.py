import pydicom
import os
import json
import numpy as np
import math
pth = '/data1/data/output/cerebral'
PTH = '/data1/liut/workspace/daan/point'
ab = 0
patientid = []
caseids = []

with open('/data1/liut/workspace/daan/ID.txt', 'r') as id_f:
        a = id_f.readlines()
for i in a:
    patientid.append(i.split('\n')[0])
for f in os.listdir(pth): 
    casedict = {}
    try:
        dcm_pth = os.path.join(pth, f, 'slices/0001.dcm')
        dt = pydicom.read_file(dcm_pth).PatientID
        if dt in patientid: 
            ab += 1
            point_json_pth = os.path.join(pth, f, 'key_point_2.json')
            point_json_pth1 = os.path.join(PTH, dt, 'key_point.json')
            type_pth = os.path.join(pth, f, 'config.json')
            caseids.append(f)

#             print(ab, casedict.keys(), dt )
########写头颈判断类型
#         with open('/data1/liut/workspace/daan/type/type.json', 'w+') as type_json:
#             type_json_data = json.dumps(type_dict, indent=2)
#             type_json.write(type_json_data)
#             print(type_dict)
########写关键点
#             with open(point_json_pth, 'r') as json_f:
#                 point_json = json.load(json_f)
#             xg_zuobiao = {}
#             for xg_name in point_json.keys():
#                 xg_zuobiao[xg_name] =  point_json[xg_name]['pos'] 
#             casedict[f] = xg_zuobiao
#             if os.path.exists(point_json_pth1) == False:
#                 with open(point_json_pth1, 'w') as load_f:
#                     casedict_json = json.dumps(casedict,indent=2)
#                     load_f.write(casedict_json)
#                 print(casedict.keys())
        
    except Exception as e:
        print(e)
    continue

################关键点##############

test_dir = '/data1/data/output/cerebral'
test_T_dir = '/data1/liut/workspace/daan/point' 
test_lst = []
count = 0
xg_t = 0 
xg_f = 0 
r = 2
for testid in caseids:
    count += 1
    test_point_pth = os.path.join(test_dir, testid, "key_point_2.json")
    test_dcm_pth = os.path.join(test_dir, testid, 'slices/0001.dcm')
    test_patientid = pydicom.read_file(test_dcm_pth).PatientID
    test_lst.append(test_patientid)
    test_point_T_pth = os.path.join(test_T_dir, test_patientid, "key_point.json")
#     print(test_point_T_pth)
    with open(test_point_pth, 'r') as test_load_json:
        test_point_json = json.load(test_load_json)
        
    with open(test_point_T_pth, 'r') as test_load_T_json:
        test_point_T_json = json.load(test_load_T_json)
        
    for test_xg in test_point_T_json[testid].keys():

        if test_xg in test_point_json.keys():
            
            x, y, z = test_point_json[test_xg]['pos']
            x1, y1, z1 = test_point_T_json[testid][test_xg]
            r1 = math.sqrt(abs(x1 - x) + abs(y1 - y) + abs(z1 - z))
            if r1 <= r:
                xg_t += 1
            else:
                xg_f += 1
                print("caseid: ", testid,
                    "\nFALSE: ", test_xg,
                    "\nTPoint", x1, y1, z1,
                    "\nFpoint", x, y, z)
        elif test_xg not in test_point_json.keys():
            print("!!!!!!case: ", testid, 
                 "\nno: ", test_xg)
print("关键点合格数/比例: ", 
      '\n', xg_t, 
      '\n{:.2%}'.format(xg_t / (xg_t + xg_f)),
      "\n关键点错误数/比例: ", 
      '\n', xg_f, 
      '\n{:.2%}'.format(1 - (xg_t / (xg_t + xg_f))))
##########头颈判断类型######
cerebral_type_json = '/data1/liut/workspace/daan/type/type.json'
with open(cerebral_type_json, 'r') as conf_f_t:
    config_info_t = json.load(conf_f_t)
#     print(config_info_t)
cerebral_type_dict =  {}
count = 0
count1 = 0
for caseid in caseids:
    conf_json_pth = os.path.join(pth, caseid, 'config.json')

    cerebral_dcm_pth  = os.path.join(pth, caseid, 'slices/0001.dcm')
    
    with open (conf_json_pth, 'r') as conf_f:
        config_info = json.load(conf_f)
    dd = pydicom.read_file(cerebral_dcm_pth).PatientID
    cerebral_type_dict[dd] = config_info['Type']
#     print(dd)


for pidt in config_info_t.keys():
#     print("Ture: ", config_info_t[pidt])
#     print("False: ", cerebral_type_dict[pidt])
    if pidt in cerebral_type_dict.keys():
        if  config_info_t[pidt] == cerebral_type_dict[pidt]:
            count += 1
        elif config_info_t[pidt] == 'all' and cerebral_type_dict[pidt] == 'neck':
            print("头颈，判断成了！！单颈！！", pidt)
        elif config_info_t[pidt] == 'all' and cerebral_type_dict[pidt] == 'head':
            print("头颈，判断成了！！单颅！！", pidt)
        elif config_info_t[pidt] == 'neck' and cerebral_type_dict[pidt] == 'head':
            print("单颈，判断成了！！单颅！！", pidt)
        elif config_info_t[pidt] == 'neck' and cerebral_type_dict[pidt] == 'all':
            print("单颈，判断成了！！头颈！！", pidt)
        elif config_info_t[pidt] == 'head' and cerebral_type_dict[pidt] == 'all':
            print("单颅，判断成了！！头颈！！", pidt)
        elif config_info_t[pidt] == 'all' and cerebral_type_dict[pidt] == 'head':
            print("单颅，判断成了！！头颈！！", pidt)
            count1 += 1
    elif pidt not in cerebral_type_dict.keys():
        print('没有找到的case',pidt)
print("正确: ", count)
print("错误: ", count1)
print("合格率: ", format((count / (count + count1)), '.2%'))

