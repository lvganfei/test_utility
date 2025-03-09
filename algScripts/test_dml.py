import os
import json
import pydicom
import csv
import math
csvpth = '/data1/liut/workspace/daan/caseid.csv'
opt = '/data1/data/output/cerebral/'
dml_pth = '/data1/liut/workspace/daan/dml'
cid_T = []  ###动脉瘤答案ID
for i in os.listdir(dml_pth):
    cid_T.append(i)
dirnames = csv.reader(open(csvpth, 'r'))
count = 0
dml_dict = {}
cid_FT = []
for dirname in dirnames:
    jspth = os.path.join(opt, dirname[0], 'diagnosis_result.json')
    try:
        with open(jspth, 'r') as js:
            test_js = json.load(js)
        for i in  test_js.keys():
            if test_js[i]['type'] == 3:
                count += 1
                cid_FT.append(dirname[0])
#     except Exception as e:
#         print(e)
    except:
        pass
# print(cid_FT,len(cid_FT),'\n+++++',cid_T,len(cid_T),'\n\n\n\n\n\n')
# print(set(cid_FT) & set(cid_T))

a0 = 0
a1 = 0
for f in set(cid_T) & set(cid_FT):
    coord_T_lst = []
    coord_F_lst = []
    testF = []
    testT = []
#     try:
    jspth_T = os.path.join(dml_pth, f, 'diagnosis_result.json')
    jspth_F = os.path.join(opt, f, 'diagnosis_result.json')

    with open(jspth_F, 'r') as js_F:
        test_js_F = json.load(js_F)
    with open(jspth_T, 'r') as js_T:
        test_js_T = json.load(js_T)

    for n in test_js_T.keys():
        if test_js_T[n]['type'] == 3:
            coord_T = test_js_T[n]['coord']
            coord_T_lst.append(coord_T)
            testT.append(coord_T)

    for m in test_js_F.keys():
#         print(f,m)
#         print(test_js_F[m]['type'])
        if test_js_F[m]['type'] == 3:
            coord_F = test_js_F[m]['coord']
            coord_F_lst.append(coord_F)
            testF.append(coord_F)

    for value_T in coord_T_lst:
        x1, y1, z1 = value_T

        for value_F in coord_F_lst:
            x, y, z = value_F
            #####‘r’动脉瘤的坐标半径
            r = math.sqrt(abs(x1 - x) + abs(y1 - y) + abs(z1 - z)) 

            if  r <= 3:
                coord_F_lst.remove(value_F)
                testT.remove(value_T)
    if len(coord_F_lst) > 0:
        a1 += 1
        
        print('\n', f,'误报: ', len(coord_F_lst), '个','\nTcoord:',coord_T_lst,'\nFcoord',coord_F_lst)
    if len(testT) > 0:
        a0 += 1
        print('\n', f,'遗漏: ', len(testT), '个','\nTcoord',testT)
# print('遗漏case: ',set(cid_T) - set(cid_FT))
# print('误报case: ',set(cid_FT) - set(cid_T))
fn = 0
for j in set(cid_T) - set(cid_FT):
#     print(j)
    new_T = os.path.join(dml_pth, j, 'diagnosis_result.json')

    with open(new_T, 'r') as nT_js:
        new_js_T = json.load(nT_js)
    print('遗漏case:',j)
    for m in new_js_T.keys():
        
        if new_js_T[m]['type'] == 3:
            fn += 1
            coord_new = new_js_T[m]['coord']
            
            
            print('坐标:',coord_new)

print('                       !!!!!!!!!!!!!!!!!!!!!!                       ')
fp1 = 0
for h in set(cid_FT) - set(cid_T):
    apath = os.path.join(opt, h, 'diagnosis_result.json')
    with open(apath, 'r') as js:
        js_value = json.load(js)
    print('误报case:',h)
    for f in js_value.keys():
        if js_value[f]['type'] == 3:
            fp1 += 1
            coord_dml = js_value[f]['coord']
            print('\n坐标: ', coord_dml)
print('真阳: ',count)
print('一共误报: ',fp1+a1)
print('一共漏了: ',fn + a0)

