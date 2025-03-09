import pandas as pd
import os
import time
from press.conf import use_logger, config
from press.DTO import ProductDataClass, PressMongo
import paramiko
import json
import subprocess
import shutil
import datetime
import psutil
import pydicom


logger = use_logger()
mc = ProductDataClass()


class ProductsCsv(object):

    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'products.csv')
        self.csv_reader = pd.read_csv(self.path, header=None)

    def shape_product(self, description):
        description = 'lung' if description == 'thoracic' else description
        pr = {}
        v_list = self.csv_reader.values.tolist()
        if description == 'dicom':
            pr['product_index'] = sorted([i for i, j in enumerate(v_list)])
            return pr, v_list
        pr['product_index'] = sorted([i for i, j in enumerate(v_list) if j[3].strip(' ') == description])
        return pr, v_list

    def get_dicom(self, des):
        dicom_list = list()
        pr, v_list = self.shape_product(des)
        for p_name, p_index in pr.items():
            for i in p_index:
                p_data = self.csv_reader[i:i+1]
                l_data = p_data.values.tolist()
                dicom_list.append(l_data[0])
        logger.info(dicom_list)
        return dicom_list


class PushFrom(object):
    def __init__(self, host, port, username, pwd):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.ssh = self.ssh_client()

    def ssh_client(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, self.port, self.username, self.pwd)
        return ssh

    def ssh_close(self):
        self.ssh.close()

    def sftp_file(self):
        url = f"{self.host}:{self.port}"
        transport = paramiko.Transport(url)
        transport.connect(username=self.username, password=self.pwd)
        sftp = paramiko.SFTPClient.from_transport(transport)
        print(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'push.py'))
        sftp.put(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'push.py'),
                 '/home/democompany/script/push.py')
        transport.close()
        logger.info(f"copy push to /home/democompany/script/push.py")

    def do_push(self, default_num, ctime):
        self.ssh.exec_command("rm -rf /home/democompany/script/progress.json")
        self.ssh.exec_command(f"python3 /home/democompany/script/push.py {default_num} {ctime}")
        while True:
            stdout = self.do_cmd('cat /home/democompany/script/progress.json')
            rev = stdout.read().decode()
            logger.info(rev)
            time.sleep(10)
            if not rev:
                continue
            if json.loads(rev).get('progress') == 'done' or 'error' in json.loads(rev).get('progress'):
                break

    def do_cmd(self, c):
        stdin, stdout, stderr = self.ssh.exec_command(c)
        return stdout


def choose_dicom(product):
    p_dicom = {
        'coronary': ['patientNum',
                     'patientName',
                     'seriesDescription',
                     'studyInstanceId',
                     ],
        'cerebral': ['patientNum',
                     'patientName',
                     'seriesDescription',
                     'studyInstanceId',
                     ],
        'thoracic': ['patientNum',
                     'patientName',
                     'seriesDescription',
                     'studyInstanceId',
                     ],
        'calcium': ['patientNum',
                    'patientName',
                    'seriesDescription',
                    'studyInstanceId',
                    ],
        'dicom': ['patientNum',
                  'patientName',
                  'studyDescription',
                  'seriesDescription',
                  'studyInstanceId',
                  'seriesInstanceId']
    }

    if not p_dicom.get(product):
        logger.info(f"{product} is not allow")
        return
    return p_dicom[product]


def compare_dicom_meta(dicom_list, product, session, case):

    if not isinstance(dicom_list, list):
        logger.error('dicom list type error')

    dicom_dict = {}
    sql_list = []
    result = True

    dicom_meta = choose_dicom(product)

    for d in dicom_list:
        dicom_dict['patientNum'] = d[0]
        dicom_dict['patientName'] = d[1]
        dicom_dict['studyDescription'] = d[2]
        dicom_dict['seriesDescription'] = d[3]
        dicom_dict['studyInstanceId'] = d[4]
        dicom_dict['seriesInstanceId'] = d[5]

        for dm in dicom_meta:
            if dicom_dict.get(dm):
                sql_list.append({dm: dicom_dict[dm]})
        logger.info(sql_list)

        try:
            revs = getattr(mc, "select_case")(sql_list, session, case)
            sql_list = []
        except Exception as e:
            if product == 'dicom':
                return
            logger.info(f'error {str(e)}')
            raise BaseException(e)

        if revs:
            ps_log(f'check csv {d[1]} pass', product)
        else:
            logger.info(f"check csv: {d[1]} fail ")
            ps_log(f'check csv {d[1]} fail !!!', product)
            result = False

    return result


def exec_cmd(c):
    if not c:
        return
    return subprocess.run(c, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


def do_remove(folder):
    if os.path.exists(folder):
        logger.info(f'prepare remove {folder}')
        shutil.rmtree(folder)


def async_remove_folder(folder, _coronary_output):
    import uuid
    from concurrent.futures import ThreadPoolExecutor
    logger.info(f'remove folder: {folder}')
    if not os.path.exists(folder):
        return True
    dst = os.path.join(_coronary_output, f'tmp-{str(uuid.uuid4())}')
    shutil.move(folder, dst)
    executor = ThreadPoolExecutor(max_workers=3)
    executor.map(do_remove, [dst])


def generate_sys_report(_num, output_dir, test_output):
    """
    生成系统报告
    :return:
    """
    now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    t1 = time.time()
    shutil.copytree(test_output, os.path.join(output_dir, 'tmp'))
    io_speed = round(845/float(time.time() - t1), 1)
    logger.info(f'GlusterFs io speed {io_speed}MB/s')
    async_remove_folder(os.path.join(output_dir, 'tmp'), output_dir)
    return [_num, psutil.virtual_memory().percent, psutil.cpu_percent(0), io_speed, now]


def ps_log(journal, product_name):
    abs_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(abs_path, f'logs/{product_name}.log')
    t_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if type(journal) == str:
        if (not os.path.exists(os.path.join(abs_path, 'logs', 'sign'))) and ('fail' in journal):
            os.mkdir(os.path.join(abs_path, 'logs', 'sign'))
        a = open(path, mode='a+')
        a.write(t_time + ' - ' + journal + '\n')
        a.close()
    else:
        journal = str(journal)
        a = open(path, mode='a+')
        a.write(t_time + ' - ' + journal + '\n')
        a.close()
    all_log(journal, product_name)


def rm_logs():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    for p in os.listdir(path):
        n_path = os.path.join(path, p)
        if os.path.isdir(n_path):
            shutil.rmtree(n_path)
        elif os.path.isfile(n_path):
            os.remove(n_path)
        else:
            continue


def all_log(arg, product):
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'products.log')
    with open(f, 'a') as fs:
        fs.write(f'{product}: {arg} \n')


def change_dicom_meta(dir_path: str, _num: str, body_part: str):
    """
    修改dicom meta信息
    :return:
    """
    from pydicom.uid import generate_uid
    logger.info(f'start change dicom meta for {dir_path}')
    if 'coronary' in dir_path:
        series_description = 'coronary'
    elif 'calcium' in dir_path:
        series_description = 'calcium'
    elif 'cerebral' in dir_path:
        series_description = 'cerebral'
    elif 'thoracic' in dir_path:
        series_description = 'thoracic'
    else:
        series_description = 'unknown'

    for dir in os.listdir(dir_path):
        root = os.path.join(dir_path, dir)
        if not os.path.isdir(root):
            continue
        study_id = generate_uid()
        series_id = generate_uid()
        logger.info(f'current path is {root}')
        for name in os.listdir(root):
            if name.endswith('.dcm'):
                try:
                    dcm_file = os.path.join(root, name)
                    date_set = pydicom.dcmread(dcm_file)
                    setattr(date_set, 'StudyInstanceUID', study_id)
                    setattr(date_set, 'SeriesInstanceUID', series_id)
                    setattr(date_set, 'PatientID', _num)
                    setattr(date_set, 'BodyPartExamined', body_part)
                    setattr(date_set, 'SeriesDescription', series_description)
                    date_set.save_as(dcm_file)
                except:
                    logger.info('Error: file format error, next file')
                    continue
                else:
                    logger.info('success change dicom meta data')

    logger.info(f'successfully remove sensitive for {dir_path}')
    return


def merge(a, b):
    """
    为了实现冠脉和钙化积分数据能够交替推送
    :param a:
    :param b:
    :return:
    """
    _tmp = (list(a), list(b))
    return [_tmp[i % 2].pop(0) if _tmp[i % 2] else _tmp[1 - i % 2].pop(0) for i in range(0, len(a) + len(b))]


def async_change_dicom(num):
    from concurrent.futures import ThreadPoolExecutor, wait
    logger.info('async change dicom start')
    executor = ThreadPoolExecutor(max_workers=2)
    logger.info(num)
    task = executor.map(change_dicom_meta, [(config.CORONARY_WORKSPACE, num, 'coronary'),
                                            (config.CALCIUM_WORKSPACE, num, 'calcium')])
    wait(task, return_when='All_COMPLETED')
    logger.info(task.result())
    logger.info('async change dicom done')


def init_job():
    logger.info("delete output, dicom original ..")
    if os.path.exists(config.CSV_FILE):
        os.remove(config.CSV_FILE)
    if os.path.exists(config.SYS_CSV_FILE):
        os.remove(config.SYS_CSV_FILE)
    abs_path = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(os.path.join(abs_path, 'logs', 'sign')):
        shutil.rmtree(os.path.join(abs_path, 'logs', 'sign'))


def rm_files_or_folder(output):
    if os.path.exists(output):
        cs = os.listdir(output)
        for c in cs:
            try:
                if os.path.isdir(os.path.join(output, c)):
                    shutil.rmtree(os.path.join(output, c))
                if os.path.isfile(os.path.join(output, c)):
                    os.remove(os.path.join(output, c))
            except:
                logger.info(f"handle error file {os.path.join(output, c)}")
                exec_cmd(f"rm -rf {os.path.join(output, c)}")


def rm_dicom():
    logger.info('rm dicom')
    rm_files_or_folder(config.DICOM_ORIGIN)
    mc.init_dicom()


def rm_redis():
    logger.info('rm redis')
    if os.path.exists('/data1/redis/appendonly.aof'):
        os.remove('/data1/redis/appendonly.aof')
    exec_cmd('kubectl rollout undo deployment/redis -n=skdefault')


def rm_rabbitmq():
    logger.info('rm rabbitmq')
    rm_files_or_folder(config.RABBIT_WORKSPACE)
    exec_cmd('kubectl rollout undo deployment/rabbitmq -n=skdefault')
    while True:
        rev = exec_cmd('kubectl rollout status deployment/rabbitmq -n=skdefault').stdout
        logger.info(f"rabbitmq undo {rev.decode()}")
        if rev and 'rolled out' in rev.decode():
            break
        time.sleep(1)


def rm_product():
    logger.info('rm product')
    rm_files_or_folder(config.CORONARY_OUTPUT)
    rm_files_or_folder(config.CORONARY_SOURCE)
    rm_files_or_folder(config.CEREBRAL_OUTPUT)
    rm_files_or_folder(config.CEREBRAL_SOURCE)
    rm_files_or_folder(config.CALCIUM_OUTPUT)
    rm_files_or_folder(config.CALCIUM_SOURCE)
    rm_files_or_folder(config.THORACIC_OUTPUT)
    rm_files_or_folder(config.THORACIC_SOURCE)


def rm_cases():
    pm = PressMongo()
    logger.info('rm cases')
    mc.init_cases(mc.coronary_session, mc.coronary_cases)
    mc.init_cases(mc.cerebral_session, mc.cerebral_cases)
    mc.init_cases(mc.calcium_session, mc.calcium_cases)
    mc.init_cases(mc.thoracic_session, mc.thoracic_cases)
    pm.remove_all_products()
    pm.create_all_products()


def rm_alg_job():
    logger.info("rm alg job")
    exec_cmd("kubectl get jobs -n=skdefault|awk '{print $1}'|"
             "grep alg|xargs -n1 -i{} kubectl delete jobs/{} -n=skdefault")


def stop_dicom_service():
    logger.info('stop dicom service')
    exec_cmd('kubectl scale --replicas=0 deployment/plt-data-service -n=skdefault')


def start_dicom_service():
    logger.info('start dicom service')
    exec_cmd('kubectl scale --replicas=1 deployment/plt-data-service -n=skdefault')
    rev = exec_cmd('kubectl rollout status deployment/plt-data-service -n=skdefault').stdout
    logger.info(f'dicom service {rev.decode()}')
    while True:
        if rev and 'successfully rolled out' in rev.decode():
            break
        time.sleep(1)


def start_nvidia_pm():
    exec_cmd("nvidia-smi -pm 1")