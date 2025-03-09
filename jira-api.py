from jira import JIRA
import datetime
import time


project_mapping = {
    "coronary": {
        "project_key": "CTA", "project_owner": "jinjie", "project_id": 10001,
    },
    "cerebral": {
        "project_key": "CEREBRAL", "project_owner": "jiangpeng", "project_id": 10301,
    },
    "ncct": {
        "project_key": "NCCT", "project_owner": "zhangsy", "project_id": 10601,
    },
    "ctp": {
        "project_key": "CTP", "project_owner": "shengdd", "project_id": 10602,
    },
    "thoracic": {
        "project_key": "THORACIC", "project_owner": "peijj", "project_id": 10304,
    },
    "cloud": {
        "project_key": "TOC", "project_owner": "shengdd", "project_id": 10604,
    },
    "platform": {
        "project_key": "PLT", "project_owner": "guyy", "project_id": 10307,
    }
}


def get_key(product, key):
    for p in project_mapping:
        if p in product:
            return project_mapping[p][key]
        elif p.startswith('plt'):
            return project_mapping['platform'][key]
        else:
            return project_mapping['cloud'][key]


class TesterJIRA(JIRA):
    """
    主要是集成jira 的session，
    jira库没有对zephyr插件做集成
    下面用到host的都是需要自己实现
    """

    def __init__(self):
        self.host = 'https://jira.democompany.net'
        self.pwd = ('victor', 'great@democompany')
        JIRA.__init__(self, server=self.host, auth=self.pwd)

    def get_dhb_duedate(self):
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        a = self._session.post(url=f"{self.host}/rest/api/2/search",
                                     json={"jql":"project = DHB and duedate <= now()"})
        res = a.json()['issues']
        # print(res)
        print(len(res))
        # issue1 = res[0]
        for i in res:
            key = i['key']
            summary = i['fields']['summary']
            print(f'{key} : {summary}')
        # for key,val in issue1.items():
        #     print(f'{key}: {val}')
            

if __name__ == '__main__':
    a = TesterJIRA()
    a.get_dhb_duedate()