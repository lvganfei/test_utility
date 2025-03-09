import json
import requests
import time
import pandas as pd
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData, create_engine

# apply a random series every 30s 
host = str(sys.argv[1])
# series_list_file=str(sys.argv[2])

PLT_ENDPOINT = 'http://10.16.10.214/api/usr/tokens'
APPLY_URL = 'http://10.16.10.214/api/dicom/series/apply/'
sql_uri = 'mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@'+host+':13306/plt_dicom?charset=utf8mb4'
USR = 'perf_test'
PWD = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
token = ''

# proxies = {'http': f'http://{host}:80'}

def login():
    headers = {"content-type": "application/json"}
    data = {"username": USR, "password": PWD}
    r = requests.post(PLT_ENDPOINT, data=json.dumps(data), headers=headers)
    # print(r.json())
    token = r.json()['token'] or 'failed'
    return token

def get_series():
    engine = create_engine(sql_uri,pool_recycle=3600, echo=False)
    Session = sessionmaker(bind=engine)

    meta = MetaData()
    meta.reflect(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    Base = automap_base(metadata=meta)
    Base.prepare()

    # Apply_record = Base.classes.t_apply_record
    # Series = Base.classes.t_series

    sql_statement = 'select series_instance_uid FROM plt_dicom.series where from_ae = "coronary" order by series_instance_uid asc'
    result = session.execute(sql_statement).fetchall()

    # result = session.query(Apply_record).filter(Apply_record.state == 'APPLIED', Apply_record.applied_services == workflow_id).order_by(Apply_record.patient_id.asc())
    # for i in result:
    #     print(i.series_instance_uid,i.workflow_id)
    return result

def get_series_from_csv(csv_path):
    data = pd.read_csv(csv_path, sep=',',header=0,usecols=[0,1,2])

    origin_arr = data.values.tolist()
    return origin_arr


def apply():
    tk = login()
    print(tk)
    headers = {"content-type": "application/json", "Authorization": "Bearer "+ tk}

    series_list = get_series_from_csv('/data1/jenkins_scripts/old_plt_mixed_press_600.csv')
    
    for series in series_list:
        series_instance_uid = series[0]
        service = series[2]

        data = {"series_id_list":[series_instance_uid],"service_name": service}
        r = requests.post(APPLY_URL + service, data=json.dumps(data),headers=headers)
        print(r.status_code)
        
    # with open(series_list_file) as series_list:
    #     count=0
    #     lines=series_list.read().splitlines()
    #     for line in lines:
    #         series_id = line
    #         service = 'thoracic'

    #         print(series_id)

    #         data = {"series_id_list":[series_id],"service_name": service}
    #         r = requests.post(APPLY_URL + service, data=json.dumps(data),headers=headers)
    #         print(r.status_code)
    #         # print(r.json())
    #         print(str(count) + 'th case apply finished')

    #         time.sleep(30)
    #         count = count + 1




if __name__ == '__main__':
    apply()

