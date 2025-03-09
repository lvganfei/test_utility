import json
import requests
import time
import sys

# apply a random series every 30s 
host = str(sys.argv[1])
series_id_path = str(sys.argv[2])
token = str(sys.argv[3])

if (host == None or series_id_path == None or token == None):
    print('miss parameter')
    sys.exit(1)

PLT_ENDPOINT = 'http://qa.platform.democompany.net/api/usr/tokens'
APPLY_URL = 'http://qa.platform.democompany.net/api/dicom/series/apply/'
GET_MERGE_SETTING = 'http://ctpdoc.qa.platform.democompany.net/api/ctp/phase_merge_setting'
sql_uri = 'mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@'+host+':17017/plt_dicom?charset=utf8mb4'



# def login():
    # headers = {"content-type": "application/json"}
    # data = {"username": USR, "password": PWD}
    # r = requests.post(PLT_ENDPOINT, data=json.dumps(data), headers=headers)
    # print(r.json())
    # global token 
    # token = r.json()['token'] or 'failed'
    # token = '52f9b304a9c04dc686d8e09173159c6b'

def switch_merge_setting(action):
    print('---------------'+token+'---------------')
    headers = {"content-type": "application/json", "Authorization": "Bearer "+ token}
    merge_settings = requests.get(GET_MERGE_SETTING,params={},headers=headers)
    setting_arr = merge_settings.json()
    print(setting_arr)
    for setting in setting_arr:
        if (action == 'start' and setting['phase_count'] != 19):
            continue
        else:
            # print('switch merge setting')
            data = {}
            r = requests.put(GET_MERGE_SETTING+'/'+ setting['id'] + '/actions/' + action, data=json.dumps(data), headers=headers)
            print(r.url)
            print(r.json())
            if ('result' not in r.json().keys()) or r.json()['result'] != True:
                return False
                # raise Exception('switch failed')
            
    return True



def apply():
    headers = {"content-type": "application/json", "Authorization": "Bearer "+ token}
    service = 'ctpdoc'

    with open(series_id_path,'r') as patient_series_list:
    # "1": [
    #     "1.3.46.670589.50.2.40090578291931555915.31401334622839924138"
    # ],
    # "2": [
    #     "1.3.46.670589.50.2.38891514242915580229.26897450402601039384"
    # ],
        single_series = []
        multi_series = []
        patient_list = json.load(patient_series_list)
        for series_ids in patient_list.values():
            if len(series_ids) == 19:
                multi_series.extend(series_ids)
            else:
                single_series.extend(series_ids)
                
            
        print(len(single_series))
        print(len(multi_series))
        
        # start apply multi series
        
        if (switch_merge_setting('start') == True):
            data = {"series_id_list":multi_series,"service_name": service}
            r = requests.post(APPLY_URL + service,data=json.dumps(data),headers=headers)
            print(r.url)
            print(r.status_code)
            print('apply multi series and wait 120s...')
        
        time.sleep(300)

        #start apply single series
        if (switch_merge_setting('stop') == True):
            
            data = {"series_id_list":single_series,"service_name": service}
            r = requests.post(APPLY_URL + service,data=json.dumps(data),headers=headers)
            print(r.url)
            print(r.status_code)
            print('apply single series and sleep 30s')
        if (switch_merge_setting('stop') == True):
            print('apply finished and stop merge')






if __name__ == '__main__':
    # login()
    apply()