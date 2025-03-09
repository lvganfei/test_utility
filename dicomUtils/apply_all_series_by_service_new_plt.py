import json
import requests
import time
import pandas as pd
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData, create_engine

# apply a random series every 30s 
host = str(sys.argv[1])

PLT_ENDPOINT = f'http://{host}/api/user/tokens'
APPLY_URL = f'http://{host}/api/platform/record/apply?workflowId='
sql_uri = 'mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@'+host+':13306/plt_universe?charset=utf8mb4'
USR = 'perf_test'
PWD = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
token = ''

WORKFLOW_ID_NAME_MAPPING = {
    "coronary": 1,
    "cerebral": 6,
    "thoracic": 9
}

def login():
    headers = {"content-type": "application/json"}
    payload = {"username": USR, "password": PWD}
    print(payload)
    r = requests.post(PLT_ENDPOINT,data=json.dumps(payload), headers=headers)
    print(r.json())
    token = r.json()["data"] or ''
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

    sql_statement = 'SELECT t_s.series_instance_uid, t_c.case_num,t_c.workflow_id FROM plt_universe.t_series as t_s, plt_universe.t_case as t_c where t_c.series_id = t_s.id and t_c.state =400'
    result = session.execute(sql_statement).fetchall()

    # result = session.query(Apply_record).filter(Apply_record.state == 'APPLIED', Apply_record.applied_services == workflow_id).order_by(Apply_record.patient_id.asc())
    # for i in result:
    #     print(i.series_instance_uid,i.workflow_id)
    return list(result)

def get_series_from_csv(csv_path):
    data = pd.read_csv(csv_path, sep=',',header=0,usecols=[0,1,2])

    origin_arr = data.values.tolist()
    return origin_arr

def apply():
    tk = login()
    print(tk)
    headers = {"content-type": "application/json", "Authorization": tk}

    # series_list = get_series_from_csv('/data1/jenkins_scripts/old_plt_mixed_press_600.csv')
    series_list = get_series()

    print(len(series_list))

    count=0
    for series in series_list:

        
        series_id = series[0]
        workflow_id = series[2]
        # workflow_name = series[2]
        # workflow_id = WORKFLOW_ID_NAME_MAPPING[workflow_name]

        print(f'series_id:{series_id}, workflow_id:{workflow_id}')
        
        
        data = {"seriesIds":[series_id],"workflowId": workflow_id, "serviceName": workflow_id}
        print(APPLY_URL + str(workflow_id))
        print(data)
        # r = requests.post(APPLY_URL + str(workflow_id), data=json.dumps(data),headers=headers)
        # print(r.status_code)
        # print(r.json())
        print(str(count) + 'th case apply finished')
    
        count = count + 1




if __name__ == '__main__':
    apply()
