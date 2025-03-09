import os
import json
import paramiko
import sshtunnel
import time
import shutil
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base


server_abs_path = '/data1/data/output'


class CoronaryTestCase(object):

    def __init__(self):
        url = "mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@127.0.0.1:23306/plt_coronary?" \
              "charset=utf8mb4&autocommit=true"
        # 创建数据库引擎
        self.engine = create_engine(url,
                                    echo=False,
                                    encoding='utf-8',
                                    pool_size=2,
                                    pool_recycle=3600)
        # 创建数据模型绑定
        self.base = automap_base()
        self.base.prepare(self.engine, reflect=True)
        self.session = self.make_session()
        self.cases = self.table('cases')

    def table(self, table_name):
        return getattr(self.base.classes, table_name)

    def make_session(self):
        session_class = sessionmaker(bind=self.engine, autocommit=True)
        session_obj = session_class()
        return session_obj

    def get_mysql_bad_case(self):
        cases = self.cases
        return self.session.query(cases.case_num,
                                  cases.state,
                                  cases.version,
                                  cases.study_identifier,
                                  cases.alg_start_at,
                                  cases.alg_finish_at,
                                  cases.image_count,).filter(
                     self.cases.state.in_(["6"])).all()

    def get_mysql_cases(self):
        cases = self.cases
        return self.session.query(cases.case_num,
                                  cases.state,
                                  cases.version,
                                  cases.study_identifier,
                                  cases.alg_start_at,
                                  cases.alg_finish_at,
                                  cases.image_count,
                                  ).filter(cases.state.in_(["2", "4"])).order_by(self.cases.state).all()

    def __del__(self):
        pass

    @staticmethod
    def to_list(result):
        return [list(r) for r in result]


class Tunnel:
    def __init__(self):
        self.server = sshtunnel.open_tunnel(
            ("tunnel.democompany.net", 50191),  # 跳板机
            ssh_username="devops1",
            ssh_password="j75yHMC8n2",
            remote_bind_address=('10.10.10.91', 13306),  # 远程的oracle服务器
            local_bind_address=('127.0.0.1', 23306),  # 开启本地转发端口
            block_on_close=False
        )
        self.server.start()
        print(self.server.is_alive)

    def close(self):
        self.server.close()


def run_bad_case():
    case_list = CoronaryTestCase().get_mysql_bad_case()
    case_mapping = {}
    for case in case_list:
        try:
            with open(os.path.join(server_abs_path, 'coronary', case, 'cta.log')) as case_file:
                case_mapping[case] = case_file.readlines()[-1]
        except Exception as e:
            print("{} {}".format(case, str(e)))
            case_mapping[case] = "script open file error"

    print(json.dumps(case_mapping, indent=4))
    with open(os.path.join(server_abs_path, 'coronary_script', 'alg_error_info.json'), 'w+') as json_file:
        json_file.write(json.dumps(case_mapping, indent=4))


def remote_job(request_case, func=None):
    print(request_case)
    with paramiko.SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("tunnel.democompany.net",
                    port=50191,
                    username="devops1",
                    password="j75yHMC8n2",
                    )
        if func:
            return func()
        else:
            ssh.exec_command(f"python3 {os.path.join(server_abs_path, 'coronary_script', 'get_badcase_info.py')} {request_case}")
            count = 0
            while True:
                if ssh.exec_command(f"cat {os.path.join(server_abs_path, 'flag')}")[1].read() == b'success':
                    stdin, stdout, stderr = ssh.exec_command(
                        f"cat {os.path.join(server_abs_path, 'coronary_script', 'alg_error_info.json')}")
                    return stdout.read()
                else:
                    count += count
                    if count > 5:
                        return b'remote job error'
                    time.sleep(1)


def csv_to_xlsx(file_name):
    if not file_name.endswith('.csv'):
        file_name = f"{file_name}.csv"
    csv_file = pd.read_csv(file_name, index_col=0)
    csv_file.to_excel(file_name.replace('.csv', '.xlsx'))
    return file_name


def copy_template(file_name):
    template = pd.ExcelFile('template.xlsx')
    template_sheet = 'Sheet1'
    target = pd.ExcelWriter(file_name)
    template.parse(template_sheet).to_excel(target, sheet_name='AlgTestData', index=False)
    target.save()


def run():
    """
    :return:
    开启隧道进行代理到本地连接mysql
    查询runcase与badcase数据记录到csv
    通过隧道连接91获取badcase ctalog内的跑挂信息
    将所有信息统计到csv
    """
    t = Tunnel()
    coronary_test_case = CoronaryTestCase()
    run_case = coronary_test_case.to_list(coronary_test_case.get_mysql_cases())
    if not run_case:
        raise BaseException(" find no case ")
    bad_case = coronary_test_case.to_list(coronary_test_case.get_mysql_bad_case())
    t.close()
    read_obj = 'case_num, state, version, study_identifier, alg_start_at, alg_finish_at, image_count, ai_time \n'
    for run_case_data in run_case:
        run_case_data.append(run_case_data[5] - run_case_data[4])
        read_obj += ','.join([str(r) for r in run_case_data]) + '\n'
    success_avg = [r[7].seconds for r in run_case]
    for bad_case_data in bad_case:
        read_obj += ','.join([str(r) for r in bad_case_data]) + '\n'
    stdout = remote_job(','.join([case[0] for case in bad_case]))
    read_obj = read_obj + f"avg_time, {sum(success_avg) / len(success_avg)}\n" + stdout.decode()
    file_name = f"{run_case[0][2].split('MODEL')[0]}".replace(' ', '')
    with open(f"{file_name}.csv", 'w+') as f:
        f.write(read_obj)
    new_file = csv_to_xlsx(file_name)
    shutil.copyfile(new_file, f"./files/{str(int(time.time()))[:8]}-{new_file}")
    # copy_template(f"{file_name}.xlsx")


if __name__ == '__main__':
    run()