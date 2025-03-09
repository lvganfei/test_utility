from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from hashlib import md5
import logging
import requests
import json
import os


logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sqlurl = "mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@10.12.10.202:13306/plt_universe?charset=utf8mb4"
dispatch_url = 'http://universe.platform.democompany.net/api/universe/dispatcher'
proxies = {'http': 'http://10.12.10.202:80'}

class DBModel(object):

    def __init__(self, url):
        # 创建数据库引擎
        engine = create_engine(url, echo=False, encoding='utf-8', pool_size=20, pool_recycle=300)

        # 创建数据模型绑定
        Base = automap_base()
        Base.prepare(engine, reflect=True)

        # 通过Base获取表属性
        self.T_series = Base.classes.t_series
        self.T_apply = Base.classes.t_apply
        self.T_study = Base.classes.t_study

        # 创建session 绑定数据库, 查询方式建议用with
        sessionClass = sessionmaker(bind=engine)
        self.session = sessionClass()

def apply():
    ist = DBModel(sqlurl)
    session = ist.session
    T_series = ist.T_series
    T_apply = ist.T_apply
    T_study = ist.T_study
    command = 'select study.study_instance_uid, series.series_instance_uid from t_study as study, t_series as series,t_apply as apply where series.id = apply.series_id and study.id = apply.study_id and apply.status = 96 and  apply.workflow_id = 1'
    result = session.execute(command).fetchall()
    
    print(len(result))

    headers = {"content-type": "application/json"}
    for ids in result:
        data = {"studyInstanceUid":ids[0],"seriesInstanceUid": ids[1], "type": "coronary"}
        r = requests.post(dispatch_url, headers=headers,data=json.dumps(data), proxies=proxies)
        print(r.status_code)

if __name__=='__main__':
    apply()