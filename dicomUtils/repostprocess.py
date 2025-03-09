import json
import requests
import time
import sys

host = str(sys.argv[1])
casenum_file=str(sys.argv[2])

PLT_ENDPOINT = 'http://platform.democompany.net/api/usr/tokens'
APPLY_URL = 'http://platform.democompany.net/api/dicom/series/apply/'
REPOSTPROCESS_URL = 'http://thoracic.platform.democompany.net/api/thoracic/case/repostprocess'
sql_uri = 'mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@'+host+':13306/plt_dicom?charset=utf8mb4'
USR = 'admin'
PWD = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
token = ''

proxies = {'http': f'http://{host}:80'}

def login():
    headers = {"content-type": "application/json"}
    data = {"username": USR, "password": PWD}
    r = requests.post(PLT_ENDPOINT, proxies=proxies, data=json.dumps(data), headers=headers)
    # print(r.json())
    token = r.json()['token'] or 'failed'
    return token

def repostprocess():
    tk = login()
    print(tk)
    headers = {"content-type": "application/json", "Authorization": "Bearer "+ tk}

    with open(casenum_file) as casenum_list:
        count=0
        lines=casenum_list.read().splitlines()
        for line in lines:
            casenum = line
            service = 'thoracic'

            print(casenum)

            data = {"case_num": casenum}
            r = requests.post(REPOSTPROCESS_URL, proxies=proxies, data=json.dumps(data),headers=headers)
            print(r.status_code)
            print(r)
            print(str(count) + 'th case re-alg finished')

            time.sleep(10)
            count = count + 1




if __name__ == '__main__':
    repostprocess()

