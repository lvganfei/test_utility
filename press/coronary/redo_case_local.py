import requests
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from concurrent import futures
import time
import warnings


warnings.filterwarnings("ignore")
host = "platform.democompany.net"
token = requests.post(f"http://{host}/api/usr/tokens",
                      json={"username": "jinjie",
                            "password": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"},
                      headers={"content-type": "application/json"}).json()['token']

auth = {'Authorization': 'Bearer ' + token}


class MysqlSession(object):

    def __init__(self, mysql):
        self.engine = create_engine(mysql, echo=False, encoding='utf-8', pool_size=10)
        # 创建数据模型绑定
        self.Base = automap_base()
        self.Base.prepare(self.engine, reflect=True)
        self.sessionClass = sessionmaker(bind=self.engine)
        self.session = self.sessionClass()

    def select_in(self, table, column, value):
        table = getattr(self.Base.classes, table)
        column = getattr(table, column)
        rev = self.session.query(table).filter(column.in_(value))
        self.session.commit()
        return rev

    def select(self, table, column, value):
        table = getattr(self.Base.classes, table)
        column = getattr(table, column)
        rev = self.session.query(table).filter(column == value).all()
        self.session.commit()
        return rev

    def update(self, table, column, value, column2, value2):
        table = getattr(self.Base.classes, table)
        column = getattr(table, column)
        column2 = getattr(table, column2)
        self.session.query(table).filter(column == value).update({column2: value2})
        self.session.commit()


def redo(case):
    print(f"redo case {case}")
    response = requests.post(url=f'http://coronary.{host}/api/coronary/case/{case}/repostprocess',
                             json={},
                             headers=auth,
                             verify=False)
    print(response.text)


def push(case):
    print(f"push {case}")
    args = {
            "data": [
                {
                    "value": [
                        {
                            "index": 0,
                            "key": f"{case}*4*LAD*0*0",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "ww": 800,
                            "wl": 300,
                            "scale": 0.21391304347826087
                        },
                        {
                            "index": 1,
                            "key": f"{case}*4*LCX*0*0",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "ww": 800,
                            "wl": 300,
                            "scale": 0.3738601823708207
                        },
                        {
                            "index": 2,
                            "key": f"{case}*4*RCA*0*0",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "ww": 800,
                            "wl": 300,
                            "scale": 0.2379110251450677
                        },
                        {
                            "index": 3,
                            "key": f"{case}*6*LAD*0*1",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "wl": 127,
                            "ww": 255,
                            "scale": 0.240234375
                        },
                        {
                            "index": 4,
                            "key": f"{case}*6*LAD*0*2",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "wl": 127,
                            "ww": 255,
                            "scale": 0.240234375
                        },
                        {
                            "index": 5,
                            "key": f"{case}*6*LAD*0*3",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "wl": 127,
                            "ww": 255,
                            "scale": 0.240234375
                        },
                        {
                            "index": 6,
                            "key": f"{case}*6*LAD*1*1",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "wl": 127,
                            "ww": 255,
                            "scale": 0.240234375
                        },
                        {
                            "index": 7,
                            "key": f"{case}*6*LAD*1*2",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "wl": 127,
                            "ww": 255,
                            "scale": 0.240234375
                        },
                        {
                            "index": 8,
                            "key": f"{case}*6*LAD*1*3",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "wl": 127,
                            "ww": 255,
                            "scale": 0.240234375
                        },
                        {
                            "index": 9,
                            "key": f"{case}*6*LCX*2*1",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "wl": 127,
                            "ww": 255,
                            "scale": 0.240234375
                        },
                        {
                            "index": 10,
                            "key": f"{case}*6*LCX*2*2",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "wl": 127,
                            "ww": 255,
                            "scale": 0.240234375
                        },
                        {
                            "index": 11,
                            "key": f"{case}*6*LCX*2*3",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "wl": 127,
                            "ww": 255,
                            "scale": 0.240234375
                        },
                        {
                            "index": 12,
                            "key": f"{case}*3*LCX*2*3",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "wl": 127,
                            "ww": 255,
                            "scale": 0.240234375
                        },
                        {
                            "index": 13,
                            "key": f"{case}*3*RCA*4*3",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "wl": 127,
                            "ww": 255,
                            "scale": 0.240234375
                        },
                        {
                            "index": 14,
                            "key": f"{case}*3**9*3",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "wl": 127,
                            "ww": 255,
                            "scale": 0.240234375
                        },
                        {
                            "index": 15,
                            "key": f"{case}*2*LAD*0*0",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "ww": 800,
                            "wl": 300,
                            "scale": 0.248046875
                        },
                        {
                            "index": 16,
                            "key": f"{case}*2*LAD*20*0",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "ww": 800,
                            "wl": 300,
                            "scale": 0.248046875
                        },
                        {
                            "index": 17,
                            "key": f"{case}*2*LCX*0*0",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "ww": 800,
                            "wl": 300,
                            "scale": 0.248046875
                        },
                        {
                            "index": 18,
                            "key": f"{case}*2*LCX*20*0",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "ww": 800,
                            "wl": 300,
                            "scale": 0.248046875
                        },
                        {
                            "index": 19,
                            "key": f"{case}*2*RCA*0*0",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "ww": 800,
                            "wl": 300,
                            "scale": 0.248046875
                        }
                    ],
                    "layout": [
                        4,
                        5
                    ]
                },
                {
                    "value": [
                        {
                            "index": 20,
                            "key": f"{case}*2*RCA*20*0",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "ww": 800,
                            "wl": 300,
                            "scale": 0.248046875
                        },
                        {
                            "index": 21,
                            "key": f"{case}*14*LAD*1*2",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "wl": 127,
                            "ww": 255,
                            "scale": 0.240234375
                        },
                        {
                            "index": 22,
                            "key": f"{case}*14*LCX*3*2",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "wl": 127,
                            "ww": 255,
                            "scale": 0.240234375
                        },
                        {
                            "index": 23,
                            "key": f"{case}*8*LAD*0*2",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "ww": 800,
                            "wl": -300,
                            "scale": 0.240234375
                        },
                        {
                            "index": 24,
                            "key": f"{case}*8*LCX*2*2",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "ww": 800,
                            "wl": -300,
                            "scale": 0.240234375
                        },
                        {
                            "index": 25,
                            "key": f"{case}*8*RCA*4*2",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                124
                            ],
                            "ww": 800,
                            "wl": -300,
                            "scale": 0.240234375
                        }
                    ],
                    "layout": [
                        4,
                        5
                    ]
                }
            ],
            "printer": "dc491e8b-bf0b-49e5-8b52-0e649a05ed6f",
            "film_size": "14INX17IN",
            "ae_id": "dc491e8b-bf0b-49e5-8b52-0e649a05ed6f"
        }
    requests.post("https://coronary.{host}/api/coronary/output/push_data",
                             json=args,
                             headers=auth,
                             verify=False)


def dcm_print(case):
    print(f"dcm print {case}")
    args = {
            "data": [
                {
                    "value": [
                        {
                            "index": 0,
                            "key": f"{case}*2*LAD*0*0",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                156
                            ],
                            "ww": 800,
                            "wl": 300,
                            "scale": 0.248046875
                        },
                        {
                            "index": 1,
                            "key": f"{case}*2*LAD*13*0",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                156
                            ],
                            "ww": 800,
                            "wl": 300,
                            "scale": 0.248046875
                        },
                        {
                            "index": 2,
                            "key": f"{case}*2*LAD*26*0",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                156
                            ],
                            "ww": 800,
                            "wl": 300,
                            "scale": 0.248046875
                        },
                        {
                            "index": 3,
                            "key": f"{case}*2*LCX*0*0",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                156
                            ],
                            "ww": 800,
                            "wl": 300,
                            "scale": 0.248046875
                        },
                        {
                            "index": 4,
                            "key": f"{case}*2*LCX*13*0",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                156
                            ],
                            "ww": 800,
                            "wl": 300,
                            "scale": 0.248046875
                        },
                        {
                            "index": 5,
                            "key": f"{case}*2*LCX*26*0",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                156
                            ],
                            "ww": 800,
                            "wl": 300,
                            "scale": 0.248046875
                        },
                        {
                            "index": 6,
                            "key": f"{case}*2*RCA*0*0",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                156
                            ],
                            "ww": 800,
                            "wl": 300,
                            "scale": 0.248046875
                        },
                        {
                            "index": 7,
                            "key": f"{case}*2*RCA*13*0",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                156
                            ],
                            "ww": 800,
                            "wl": 300,
                            "scale": 0.248046875
                        },
                        {
                            "index": 8,
                            "key": f"{case}*2*RCA*26*0",
                            "transition": [
                                1,
                                1,
                                0,
                                0,
                                127,
                                156
                            ],
                            "ww": 800,
                            "wl": 300,
                            "scale": 0.248046875
                        }
                    ],
                    "layout": [
                        4,
                        4
                    ]
                }
            ],
            "printer": "547537b8-a574-8e5d-4aef-dfe06289d5c1",
            "film_size": "14INX17IN",
            "ae_id": "547537b8-a574-8e5d-4aef-dfe06289d5c1"
        }
    requests.post(f"https://coronary.{host}/api/coronary/case/{case}/print",
                  json=args,
                  headers=auth,
                  verify=False)


def shift(case):
    requests.post(url=f'http://coronary.platform.democompany.net/api/coronary/case/{case}/process',
                  json={"action": "shift"},
                  headers=auth)
    print(case)


if __name__ == '__main__':
    session = MysqlSession('mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@10.10.10.93:13306/plt_coronary?charset=utf8mb4')
    result = []
    with futures.ThreadPoolExecutor(max_workers=20) as executor:
        for c in [i.case_num for i in session.select_in('cases', 'state', [11, 1, 2, 3, 4, 5, 6, 12])]:
            f = executor.submit(redo, c)
            result.append(f)
        futures.as_completed(result)
