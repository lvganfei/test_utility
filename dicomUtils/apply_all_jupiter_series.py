import json
import requests
import time
import sys
# import sqlalchemy
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy import MetaData, create_engine

# apply a random series every 30s 
host = str(sys.argv[1])
series_id_path = str(sys.argv[2])

PLT_ENDPOINT = 'http://platform.democompany.net/api/usr/tokens'
APPLY_URL = 'http://platform.democompany.net/api/dicom/series/apply/'
sql_uri = 'mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@'+host+':13306/plt_dicom?charset=utf8mb4'
USR = 'perf_test'
PWD = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
token = ''

proxies = {'http': 'http://'+ host +':80'}

# def get_series():
#     engine = create_engine(sql_uri,pool_recycle=3600, echo=False)
#     Session = sessionmaker(bind=engine)

#     meta = MetaData()
#     meta.reflect(bind=engine)

#     Session = sessionmaker(bind=engine)
#     session = Session()

#     Base = automap_base(metadata=meta)
#     Base.prepare()

#     Series = Base.classes.series

#     result = session.query(Series.patient_id).filter(Series.modality == 'MR').group_by(Series.patient_id.asc())
#     for i in result:
#         print(i.patient_id,i.applied_services)
#     return result

def login():
    headers = {"content-type": "application/json"}
    data = {"username": USR, "password": PWD}
    r = requests.post(PLT_ENDPOINT, proxies=proxies, data=json.dumps(data), headers=headers)
    # print(r.json())
    token = r.json()['token'] or 'failed'
    return token

def apply():
    tk = login()
    print(tk)
    headers = {"content-type": "application/json", "Authorization": "Bearer "+ tk}

    with open(series_id_path,'r') as patient_series_list:
        patient_list = json.load(patient_series_list)

        count=0
        for series_ids in patient_list.values():
        
            data = {"series_id_list":series_ids,"service_name": "jupiter"}
            r = requests.post(APPLY_URL + "jupiter",proxies=proxies, data=json.dumps(data),headers=headers)
            print(r.status_code)
            # print(r.json())
            print(str(count) + 'th case apply finished')
        
            time.sleep(60)
            count = count + 1




if __name__ == '__main__':
    apply()
