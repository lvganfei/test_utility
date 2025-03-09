import os
import re
import json
import datetime
from press.conf import config
from press.common import ps_log
from press.conf import use_logger


logger = use_logger()


def calculate_alg():
    pattern = re.compile('All\s+Completed\s+in\s+(\d+\.\d+).*!!')
    path = config.PRODUCTS_OUTPUT
    d = {}

    for p in os.listdir(path):
        d[p] = {}
        if not os.path.isdir(os.path.join(path, p)):
            continue
        for case in os.listdir(os.path.join(path, p)):
            if os.path.isdir(os.path.join(path, p, case)):
                case_path = os.path.join(path, p, case)
                if p == 'coronary':
                    log = os.path.join(case_path, 'cta.log')
                elif p == 'cerebral':
                    log = os.path.join(case_path, 'cerebral.log')
                elif p == 'thoracic':
                    log = os.path.join(case_path, 'chest_lung.log')
                else:
                    continue
                if log:
                    time_struct = os.path.getctime(case_path)
                    file_create_time = datetime.datetime.fromtimestamp(time_struct)
                    if file_create_time <= datetime.datetime.strptime('2019-12-27 00:00:00', '%Y-%m-%d %H:%M:%S'):
                        continue
                    if not os.path.exists(os.path.join(case_path, log)):
                        d[p][case] = 'miss log file'
                        continue
                    else:
                        with open(os.path.join(case_path, log)) as af:
                            line = af.readlines()[-1].strip('\n')
                            result = re.findall(pattern, line)
                        if len(result) > 0:
                            dcm_count = len([l for l in os.listdir(os.path.join(case_path, 'slices')) if 'dcm' in l])
                            result.append(dcm_count)
                            result.append(round(result[1]/float(result[0]), 1))
                            d[p][case] = result
                        else:
                            d[p][case] = str(line) if len(line) > 0 else 'log context is none'

    for product in d:
        alg_count, dcm_count, counter = 0.0, 0.0, 0
        if product not in ('coronary', 'cerebral', 'thoracic'):
            continue
        length = len(d[product])
        for case in d[product]:
            num = d[product][case]
            if isinstance(num, str):
                counter += counter
                continue
            alg_count += float(num[0])
            dcm_count += float(num[1])

        ps_log('-'*100, product)
        ps_log(json.dumps(d[product], indent=4), product)
        ps_log(f"算法总时间 {alg_count}, 原片切片总数 {dcm_count} "
               f"算法总时间/原片切片总数 {str(dcm_count / alg_count)}, "
               f"算法总时间/跑出的病例 {str(alg_count / (length - counter))}", product)

