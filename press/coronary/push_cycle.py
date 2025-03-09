import requests
from press.coronary.redo_case_local import MysqlSession


series_id = '1.2.840.113619.2.359.3.209782018.950.1550132722.461'
host = "toc.stg.platform.democompany.net"
token = requests.post(f"http://{host}/api/usr/tokens",
                      json={"username": "peij",
                            "password": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"},
                      headers={"content-type": "application/json"}).json()['token']

auth = {'Authorization': 'Bearer ' + token}


def _push():
    response = requests.post('http://'+host+'/api/dicom/v1/series/apply/coronary',
                             json={"seriesIds": [series_id],
                                   "serviceName": "coronary"},
                             headers=auth).json()
    print(response)


if __name__ == '__main__':
    _push()
    print("push case")
    session = MysqlSession('mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@109.244.38.201:31238/plt_coronary?charset=utf8mb4')
    print(f"select case {series_id}")
    while True:
        if session.select('cases', 'identifier', series_id)[0].state == 2:
            print(f"push {series_id}")
            _push()
            break
