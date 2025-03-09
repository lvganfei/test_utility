import json
import requests
import sys

host = str(sys.argv[1])
case_num = str(sys.argv[2])

proxies = {'http': f'{host}:80'}
PLT_ENDPOINT = 'http://platform.democompany.net/api/usr/tokens'
THORACIC_SETTING_URL = 'http://thoracic.platform.democompany.net/api/thoracic/setting/thoracic_setting'
THORACIC_URL = 'http://thoracic.platform.democompany.net/api/'
USR = 'perf_test'
PWD = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'

def login():
    headers = {"content-type": "application/json"}
    data = {"username": USR, "password": PWD}
    r = requests.post(PLT_ENDPOINT, proxies=proxies, data=json.dumps(data), headers=headers)
    # print(r.json())
    # global token 
    return r.json()['token'] or 'failed'

def get_setting(token):
    # token = login()
    headers = {"content-type": "application/json","Authorization": "Bearer "+ token}
    r = requests.get(THORACIC_SETTING_URL, proxies=proxies, headers=headers)
    # print(r.status_code)
    print(r.json()['thoracic_confidence_standard'])
    return r.json()['thoracic_confidence_standard']

def get_nodule(token):
    # token = login()
    headers = {"content-type": "application/json","Authorization": "Bearer "+ token}
    r = requests.get(f"{THORACIC_URL}/thoracic/thoracic/nodule/{case_num}", proxies=proxies, headers=headers)
    # print(r.status_code)
    return r.json()

def get_node_confidence(tag):
    mappings = {
        1: "SN",
        2: "PSN",
        3: "GGN",
        4: "CALCIUM"
    }
    return mappings.get(tag,None)


def verify_node_list():
    token = login()
    a = get_nodule(token)
    settings = get_setting(token)
    # SN = settings['SN']
    # PSN = settings['PSN']
    # GGN = settings['GGN']
    # CALCIUM = settings['CALCIUM']

    # print(a['8']['confidence'])
    # print('===============================================')
    # print(str(SN['l_3'])+' '+str(SN['m_3_l_4']) + ' ' + str(SN['m_4']))

    count = {
        "SN": 0,
        "PSN": 0,
        "GGN": 0,
        "CALCIUM": 0
    }

    nodule_idx = {
        "SN": [],
        "PSN": [],
        "GGN": [],
        "CALCIUM": []
    }

    except_num = 0

    print(len(a))

    for i in a:
        confidence = a[i]['confidence']
        tag = a[i]['tag']
        max_diam = a[i]['max_diameter']
        node_type = get_node_confidence(tag)

        print('===============================================')
        # print(tag)
        # print(node_type)
        
        l_3 = settings[node_type]['l_3']
        m_3_l_4 = settings[node_type]['m_3_l_4']
        m_4 = settings[node_type]['m_4']


        if (max_diam < 3 and confidence >= l_3):
            count[node_type] = count[node_type] + 1
            nodule_idx[node_type].append(a[i]['range_z'])
        elif (max_diam >= 3 and max_diam < 4 and confidence >= m_3_l_4):
            count[node_type] = count[node_type] + 1
            nodule_idx[node_type].append(a[i]['range_z'])
        elif (max_diam >= 4 and confidence >= m_4):
            count[node_type] = count[node_type] + 1
            nodule_idx[node_type].append(a[i]['range_z'])
        else:
            print('exception here')
            print('max_diam: '+ str(max_diam))
            print('confidence: ' + str(confidence))
            except_num = except_num + 1
        # if (tag == 1 and float(confidence) > 0.58):
        #     count=count+1
        #     print('index: '+ str(int(i)+1))
        #     print('tag: ' + str(tag))
        #     print('confidence: '+ str(confidence))
        #     print(max_diam)
        #     print(min_diam)

    # for idx in nodule_idx:
    #     nodule_idx[idx].sort()
    print(nodule_idx)
    print(count)
    print(except_num)

verify_node_list()