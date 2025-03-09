import json
import requests
import time
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData, create_engine

# apply a random series every 30s 
host = str(sys.argv[1])

PLT_ENDPOINT = 'http://platform.democompany.net/api/usr/tokens'
APPLY_URL = 'http://platform.democompany.net/api/dicom/series/apply/'
sql_uri = 'mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@'+host+':13306/plt_dicom?charset=utf8mb4'
USR = 'perf_test'
PWD = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
token = ''

proxies = {'http': f'http://{host}:80'}

def get_series():
    engine = create_engine(sql_uri,pool_recycle=3600, echo=False)
    Session = sessionmaker(bind=engine)

    meta = MetaData()
    meta.reflect(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    Base = automap_base(metadata=meta)
    Base.prepare()

    Series = Base.classes.series

# 获取所有分发到子产品的序列，除了CTP的序列，ctp的单独处理。
    result = session.query(Series).filter(Series.state == 'APPLIED', Series.applied_services.in_(['coronary','cerebral','thoracic'])).order_by(Series.series_time.asc())
    for i in result:
        print(i.series_instance_uid,i.applied_services)
    return result

def login():
    headers = {"content-type": "application/json"}
    data = {"username": USR, "password": PWD}
    r = requests.post(PLT_ENDPOINT,proxies=proxies, data=json.dumps(data), headers=headers)
    # print(r.json())
    token = r.json()['token'] or 'failed'
    return token

def apply():
    tk = login()
    print(tk)
    headers = {"content-type": "application/json", "Authorization": "Bearer "+ tk}

    series_list = get_series()
    
    count=0
    for series in series_list:

        series_id = series.series_instance_uid
        service = series.applied_services

        print(series_id)
        
        if ',' in service:
            service = service.split(',')[0]
        print(service)
        data = {"series_id_list":[series_id],"service_name": service}
        r = requests.post(APPLY_URL + service, proxies=proxies, data=json.dumps(data),headers=headers)
        print(r.status_code)
        # print(r.json())
        print(str(count) + 'th case apply finished')
    
        time.sleep(30)
        count = count + 1




if __name__ == '__main__':
    apply()
