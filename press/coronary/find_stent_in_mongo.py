import json
import os
from sk_pymongo import SkPyMongo
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine


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

    def select_like(self, table, column, value):
        table = getattr(self.Base.classes, table)
        column = getattr(table, column)
        rev = self.session.query(table).filter(column.like(f'%{value}%')).order_by(table.patient_num).all()
        self.session.commit()
        return rev

    def select_like_in(self, table, column, value, column2, value_list):
        table = getattr(self.Base.classes, table)
        column = getattr(table, column)
        column2 = getattr(table, column2)
        rev = self.session.query(table).\
            filter(column.like(f'%{value}%')).\
            filter(column2.in_(value_list)).order_by(table.patient_num).all()
        self.session.commit()
        return rev

    def update(self, table, column, value, column2, value2):
        table = getattr(self.Base.classes, table)
        column = getattr(table, column)
        column2 = getattr(table, column2)
        self.session.query(table).filter(column == value).update({column2: value2})
        self.session.commit()


mysql_session = MysqlSession('mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@109.244.38.201:32198/plt_coronary?charset=utf8mb4')
stend_cases = [c.case_num for c in mysql_session.select_like_in('cases', 'patient_num', 'stand', 'state', ['2', '4', '5', '6'])]
print(f"stend case length {len(stend_cases)}")
# 开始脚本检查支架数据是否正确
stend_cases_alg = 125
if len(stend_cases) < stend_cases_alg:
    raise BaseException("stend case is miss, please check")
cases = [c.case_num for c in mysql_session.select_like('cases', 'patient_num', 'stand')]
mongo = SkPyMongo("mongodb://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@109.244.38.201:30746/plt_coronary")
local_path = os.path.dirname(os.path.abspath(__file__))
ground_truth_result = json.load(open(os.path.join(local_path, 'ground_truth.json')))
file_obj = dict()
pre_case_stend = [
    'T20200723192738H27a3ecd2',
    'T20200724095459H4a4172a4',
    'T20200723192949H54405ccf',
    'T20200724095459Ha5c88a54',
    'T20200724095459Hc5548e7d',
    'T20200723193140H1771d02f',
    'T20200724095459H338538c1',
    'T20200724095459H4739df92',
    'T20200723193727Hdb568a01',
    'T20200723193807Hb6296b60',
    'T20200723194233H85df8304',
    'T20200724095459H4d0179a3',
    'T20200723194444H2a4b5d75',
    'T20200723194529H46b3e3e3',
    'T20200723194620H04f99326',
    'T20200720171034H613a74fc',
    'T20200720171301H6fa27178',
    'T20200720172153H23972a65',
    'T20200720171412H87092c1b',
    'T20200721191750Hd609b518',
    'T20200721191816Hebad4bcc',
    'T20200721191926H0bc75492',
    'T20200721192102H7e1dac47',
    'T20200722113834H5fc404e5',
    'T20200722162846Hea63ccd6',
    'T20200722114201H08189ff1',
    'T20200729203101Haea1ecee',
    'T20200729203216Hb00688fa',
    'T20200729203321H05923db4',
    'T20200729203411H346d87f7',
    'T20200729203536He3a5658d',
    'T20200729203855H42e69d1b',
    'T20200729203807Hf02429c8',
    'T20200729204012H913d8a0d',
    'T20200729204247H96652903',
    'T20200729204447H21221b56',
    'T20200729204633H26fc40c2',
    'T20200729204813H7ba29061',
    'T20200729205018Hf0e710ca',
    'T20200729205123Hce091f85',
    'T20200729205243Hc2f700bb',
    'T20200729205419H6bd6a401',
    'T20200729205529H5528eaad',
    'T20200729205734Hc940f0b0',
    'T20200729205929H56272a15',
    'T20200729210055Ha03d6d42'

]


def get_result():
    for case in cases:
        meta = mongo.db.metas.find_one({'case_num': case})
        if not meta:
            print(f'{case} not exits')
            continue
        if not meta:
            continue
        if not meta.get('report'):
            continue
        report = meta['report']
        if report['vessels']:
            print('mongo case_num', meta['case_num'])
            vessels = report['vessels']
            stent_json = {}
            for vessel in vessels:
                if 'unknown' in vessel:
                    continue
                mark_list, mark_dict = [], dict()
                for section in vessels[vessel]:
                    for mark in vessels[vessel][section]:
                        if mark.get('stent'):
                            if {section: 1} not in mark_list:
                                mark_list.append({section: 1})
                                mark_dict[section] = 1
                if mark_dict:
                    stent_json[vessel] = mark_dict
            if stent_json:
                file_obj[case] = stent_json
    with open(os.path.join(local_path, 'mongo_stend.json'), 'w+') as file:
        file.write(json.dumps(file_obj, indent=2))
    return file_obj


def ms_compare_case():
    back_up = [{c.case_num: c.identifier} for c in mysql_session.select_like('cases', 'patient_num', 'stand')]
    with open('back_up.json', 'w+') as back_up_file:
        back_up_file.write(json.dumps(back_up, indent=4))
    fail_list = []
    for c in pre_case_stend:
        if c not in cases:
            fail_list.append(c)
    print(fail_list)


def get_case_section():
    vessel_count, section_count = 0, 0
    for case in cases:
        meta = mongo.db.metas.find_one({'case_num': case})
        if not meta:
            print(f'{case} not exits')
            continue
        print('case_num', meta['case_num'])
        if not meta:
            continue
        if not meta.get('report'):
            continue
        report = meta['report']
        vessels = report['vessels']
        for vessel in vessels:
            if 'unknown' in vessel:
                continue
            vessel_count = vessel_count+1
            vessel_section_count = len(vessels[vessel])
            section_count = section_count+vessel_section_count
    print(vessel_count, section_count)


def compare_case():
    # 正确检查支架 tp, state = 1
    # 误报支架 fp, state = 2
    # 漏报支架 fn,  state = 3

    # 获取带支架的mongo数据
    mongo_results = get_result()
    if not mongo_results:
        return
    ground_truth_case_list = [ground_truth_case for ground_truth_case in ground_truth_result]
    for mongo_case in mongo_results:
        # 未找到ground_truth里面的case， 那就是误报支架， 修改状态为2
        if mongo_case not in ground_truth_case_list:
            print(f"case not found in ground truth {mongo_case}, --> state 2")
            for mongo_vessel in mongo_results[mongo_case]:
                for mongo_section in mongo_results[mongo_case][mongo_vessel]:
                    mongo_results[mongo_case][mongo_vessel][mongo_section] = 2
        # 进行每个mongo_case与ground_truth_case进行对比，mongo有，ground_truth无，则为误报
        else:
            for mongo_vessel in mongo_results[mongo_case]:
                # 误报支架血管未找到
                if not ground_truth_result[mongo_case].get(mongo_vessel):
                    for mongo_section in mongo_results[mongo_case][mongo_vessel]:
                        mongo_results[mongo_case][mongo_vessel][mongo_section] = 2
                    continue
                # 血管分段未找到支架
                for mongo_section in mongo_results[mongo_case][mongo_vessel]:
                    if not ground_truth_result[mongo_case][mongo_vessel].get(mongo_section):
                        mongo_results[mongo_case][mongo_vessel][mongo_section] = 2

    # 检出漏报
    mongo_loss_case = list()
    for ground_truth_case in ground_truth_result:
        # case 未在mongo找到， 漏报
        if not mongo_results.get(ground_truth_case):
            print(f"case not found in mongo {ground_truth_case} --> state 3")
            mongo_loss_case.append(ground_truth_case)
            mongo_results.update({ground_truth_case: ground_truth_result[ground_truth_case]})
            for v in mongo_results[ground_truth_case]:
                for s in mongo_results[ground_truth_case][v]:
                    mongo_results[ground_truth_case][v][s] = 3
            continue

        for ground_truth_vessel in ground_truth_result[ground_truth_case]:
            # case血管未在mongo找到， 漏报
            if not mongo_results[ground_truth_case].get(ground_truth_vessel):
                mongo_results[ground_truth_case].update({ground_truth_vessel: {}})
                for ground_truth_section in ground_truth_result[ground_truth_case][ground_truth_vessel]:
                    mongo_results[ground_truth_case][ground_truth_vessel].update({ground_truth_section: 3})
                continue
            # case 分段未在mongo找到， 漏报
            for ground_truth_section in ground_truth_result[ground_truth_case][ground_truth_vessel]:
                if not mongo_results[ground_truth_case][ground_truth_vessel].get(ground_truth_section):
                    mongo_results[ground_truth_case][ground_truth_vessel].update({ground_truth_section: 3})

    with open(os.path.join(local_path, 'stend_result.json'), 'w+') as sfile:
        sfile.write(json.dumps(mongo_results, indent=4))
    print(f"ground truth result {json.dumps(ground_truth_result, sort_keys=True)}")
    print(f"stend_result {json.dumps(mongo_results, sort_keys=True)}")
    print(f"length ground true: {len(ground_truth_result)}, stend_result: {len(mongo_results)}")


if __name__ == '__main__':
    compare_case()


