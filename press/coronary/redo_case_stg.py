import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from concurrent import futures
import pandas as pd


env = input("env: ")

if env == 'stg':
    env_mysql_port = '31352'
    pwd = 'e10adc3949ba59abbe56e057f20f883e'
else:
    env = 'uat'
    env_mysql_port = '32198'
    pwd = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'

host = f'http://coronary.{env}.platform.democompany.net'

try:
    token = requests.post(f"http://{env}.platform.democompany.net/api/usr/tokens",
                          json={"username": "jinjie",
                                "password": pwd},
                          headers={"content-type": "application/json"})
    token = 'Bearer ' + token.json()['token']
except:
    token = input("token: ")

auth = {'Authorization': token}


class MysqlSession(object):

    def __init__(self, mysql):
        self.engine = create_engine(mysql, echo=False, encoding='utf-8', pool_size=10)
        # 创建数据模型绑定
        self.Base = automap_base()
        self.Base.prepare(self.engine, reflect=True)
        self.sessionClass = sessionmaker(bind=self.engine)
        self.session = self.sessionClass()

    def select(self, table, column, value):
        table = getattr(self.Base.classes, table)
        column = getattr(table, column)
        rev = self.session.query(table).filter(column.in_(value))
        self.session.commit()
        return rev


def redo(case):
    print(case)
    print(requests.post(url=f'{host}/api/coronary/case/{case}/repostprocess',
                        json={},
                        headers=auth).text)


def shift(case):
    print(requests.post(url=f'{host}/api/coronary/case/{case}/process',
                        json={"action": "shift"},
                        headers=auth).text)


def redo_156_case():
    from press.coronary import redo_156_case_list
    for case in redo_156_case_list:
        print(requests.post(f"http://125.208.24.156:6988/api/case/{case}/repostprocess",
                            json={},
                            headers={"Authorization": "d7236989473747ebbba8f13fd4e8d7a9"}).text)


def shift_cto_case():
    from press.coronary import cto_case_list
    for case in cto_case_list:
        shift(case)


def get_csv_case():
    data = pd.read_excel(io='/Users/jinjie/日常/冠脉算法/0.99.5.cd0e6541冠脉算法各项合格率统计文档.xlsx',
                         sheet_name='结果记录表',
                         usecols='B')
    return [d[0] for d in data.values.tolist() if type(d[0]) == str]


if __name__ == '__main__':
    session = MysqlSession(f'mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@109.244.38.201:'
                           f'{env_mysql_port}/plt_coronary?charset=utf8mb4')

    with futures.ThreadPoolExecutor(max_workers=30) as executor:
        for c in [i.case_num for i in session.select('cases', 'state', [2, 3, 4, 5, 6, 11])]:
            f = executor.submit(redo, c)
    #for case in reversed([c.split(', ')[-1] for c in get_csv_case()]):
    #    shift(case)


