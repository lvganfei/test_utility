import hashlib
import numpy as np
import os
import json
import sys



compare_category = ['meta.npy',
    'result/overview.json',
    'result/emphysema_mask.npy',
    'result/overview.json',
    'result/bronchus.npz',
    'result/mask.npz',
    'result/pulmonary.npz',
    'result/case_mpr.json',
    'result/case_mpr.npy',
    'result/mask_original.npz',
    'result/bone_centerness.npy',
    'result/full_seg.seg.npz',
    'result/full_seg.seg.json',
    'result/bed_mask.npz',
    'result/bed_mask.json',
    'result/fracture_overview.json',
    'bone_stl/jianjiagu.json',
    'bone_stl/leigu.json',
    'bone_stl/suogu.json',
    'bone_stl/xionggu.json',
    'bone_stl/zhuigu.json',
    'lobe_stl/left_down.stl',
    'lobe_stl/left_up.stl',
    'lobe_stl/right_down.stl',
    'lobe_stl/right_middle.stl',
    'lobe_stl/right_up.stl',
    ]





def md5_func(path):
    with open(path, 'rb') as fp:
        data = fp.read()
        fp.close()

    md5_value = hashlib.md5(data).hexdigest()
    print(path + ': '+ md5_value)

    return md5_value


def compare_consistency(casenum_list, BASE_PATH1, BASE_PATH2, version):
    strong_compare_result = {}
    weak_compare_result = {}
    for case in casenum_list:
        case_path1 = os.path.join(BASE_PATH1, case)
        case_path2 = os.path.join(BASE_PATH2, case)
        strong_compare_result[case] = {}
        weak_compare_result[case] = {}

        for file in compare_category:
            
            file_path1 = os.path.join(case_path1, file)
            file_path2 = os.path.join(case_path2, file)
            result1 = md5_func(file_path1)
            result2 = md5_func(file_path2)
            if ( result1 == result2):
                strong_compare_result[case][file] = 'true'
            else:
                print(result1)
                print(result2)
                strong_compare_result[case][file] = 'false'
                
                if (file_path1.find('json') > 0):
                    print('not consistent, compare weak consistency')
                    weak_compare_result[case][file] = compare_json_result(file_path1, file_path2)
                else:
                    print('not consistent and not json, compare weak consistency')
               
   

    print(strong_compare_result)
    print(weak_compare_result)
    with open(f'./strong_consistency_result_{version}_cases.json', 'w') as strong_result_file:
        json.dump(strong_compare_result,strong_result_file)
        strong_result_file.close()
    with open(f'./weak_consistency_result_{version}_cases.json', 'w') as weak_result_file:
        json.dump(weak_compare_result,weak_result_file)
        weak_result_file.close()

def compare_json_result(jsonpath1='', jsonpath2=''):
    print(jsonpath1 +' '+jsonpath2)
    with open(jsonpath1, 'r') as json1:
        obj1 = json.load(json1)
    with open(jsonpath2, 'r') as json2:
        obj2 = json.load(json2)

    weak_compare_result = {}
    if (jsonpath1.find('fracture_overview') > 0):
        print('fracture overview') 
        if (len(obj1) != len(obj2)):
            print('长度不同，待完善')
        else:
            print('长度相同')
            for i in range(len(obj1)):
                weak_compare_result['confidence_original_detect_diff'] = abs(float(obj1[i]['confidence_original_detect']) - float(obj2[i]['confidence_original_detect']))
                weak_compare_result['confidence_diff'] = abs(float(obj1[i]['confidence']) - float(obj2[i]['confidence']))
                weak_compare_result['range_z_diff'] = float(sum(map(abs,(np.array(obj1[i]['range_z']) - np.array(obj2[i]['range_z'])))))
                weak_compare_result['range_x_diff'] = float(sum(map(abs,(np.array(obj1[i]['range_x']) - np.array(obj2[i]['range_x'])))))
                weak_compare_result['range_y_diff'] = float(sum(map(abs,(np.array(obj1[i]['range_y']) - np.array(obj2[i]['range_y'])))))
        return weak_compare_result
    elif (jsonpath1.find('overview.json') > 0):
        print('thoracic overview')
        if (len(obj1) != len(obj2)):
            print('长度不同，待完善')
        else:
            print('长度相同')
            for i in range(len(obj1)):
                weak_compare_result['max_diameter_diff'] = abs(float(obj1[i]['max_diameter']) - float(obj2[i]['max_diameter']))
                weak_compare_result['volume_diff'] = abs(float(obj1[i]['volume']) - float(obj2[i]['volume']))
                weak_compare_result['min_diameter_diff'] = abs(float(obj1[i]['min_diameter']) - float(obj2[i]['min_diameter']))
                weak_compare_result['confidence_diff'] = abs(float(obj1[i]['confidence']) - float(obj2[i]['confidence']))
                weak_compare_result['Dimension_max_diameter_diff'] = abs(float(obj1[i]['3D_max_diameter']) - float(obj2[i]['3D_max_diameter']))
        return weak_compare_result
    else:
        print('orther json')
        
    

# compare value in overview.json and fracture_overview.json
# def weak_consistency(casenum_list):
#     compare_item = ['result/overview.json','result/fracture_overview.json']
#     compare_result = {}
#     for case in casenum_list:
#         case_path1 = os.path.join(BASE_PATH1, case)
#         case_path2 = os.path.join(BASE_PATH2, case)
        
#         compare_result[case] = {}

#         for item in compare_item:
#             compare_result[case][item] = {}
#             item_path1 = os.path.join(case_path1, item)
#             item_path2 = os.path.join(case_path2, item)
#             compare_result[case][item] = compare_json_result(item_path1, item_path2)
   

#     print(compare_result)
    

if __name__ == '__main__':

    PATH1 = sys.argv[1] or '/data1/jenkins-script/thoracic-3in1/3in1_cases'
    PATH2 = sys.argv[2] or '/data1/jenkins-script/thoracic-3in1/2070_cases/76494f347.engineering-test'
    version = sys.argv[3]
    compare_consistency(os.listdir(PATH1), PATH1, PATH2, version)