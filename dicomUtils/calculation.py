import os
import re
import json
import time
import datetime


coronary_pattern = re.compile('All\s+Completed\s+in\s+(\d+\.\d+).*!!')
calcium_pattern = re.compile('ct_cal\s+finish\s+in\s+(\d+\.\d+).*')
cerebral_pattern = re.compile('All\s+Completed\s+in\s+(\d+\.\d+).*!!')
thoracic_pattern = re.compile('All\s+Completed\s+in\s+(\d+\.\d+).*!!')

path = '/nfs/platform-stg-lvm/data/output'
d = {}


for p in os.listdir(path):
    d[p] = {}
    if not os.path.isdir(os.path.join(path, p)):
        continue
    for case in os.listdir(os.path.join(path, p)):
        if os.path.isdir(os.path.join(path, p, case)):
            case_path = os.path.join(path, p, case)
            print(case_path)
            log = ''
            if p == 'coronary':
                log = os.path.join(case_path, 'cta.log')
            # elif p == 'cerebral':
            #     log = os.path.join(case_path, 'cerebral.log')
            # elif p == 'thoracic':
            #     log = os.path.join(case_path, 'chest_lung.log')
            else:
                continue
            if log:
                time_struct = os.path.getctime(case_path)
                file_create_time = datetime.datetime.fromtimestamp(time_struct)
                if file_create_time <= datetime.datetime.strptime('2019-12-27 00:00:00', '%Y-%m-%d %H:%M:%S'):
                    continue
                if not os.path.exists(os.path.join(case_path, log)):
                    d[p][case] = 'Log_None'
                    continue
                else:
                    with open(os.path.join(case_path, log)) as af:
                        line = af.readlines()[-1].strip('\n')
                        result = re.findall(coronary_pattern, line)
                    if len(result) > 0:
                        d[p][case] = result
                        dcm_count = len([l for l in os.listdir(os.path.join(case_path, 'slices')) if 'dcm' in l])
                        result.append(dcm_count)
                        result.append(result[1]/float(result[0]))

with open('a.json', 'w+') as jf:
    jf.write(json.dumps(d, indent=4))

alg_count, dcm_count = 0.0, 0.0

for product in d:
    if product != 'coronary':
        continue
    length = len(d[product])
    for case in d[product]:
        num = d[product][case]
        print(num)
        alg_count += float(num[0])
        dcm_count += float(num[1])

    print("alg_count {}, dcm_count {} d/a {}, a/length {}".format(alg_count, dcm_count, dcm_count/alg_count, alg_count/length))
