# -*- coding: utf-8 -*-
import time
import os
import datetime
import json
from sk_dicom_interface.storescu import StoreScu
from press.DTO import ProductDataClass
from press.assertion import products_assert
from press.common import (PushFrom, exec_cmd, rm_logs, rm_cases,
                          rm_rabbitmq, rm_redis, rm_alg_job, rm_dicom,
                          rm_product, start_dicom_service, stop_dicom_service, change_dicom_meta, start_nvidia_pm)
from press.conf import config, use_logger
from press.calculate import calculate_alg
from concurrent import futures
from press.background_schedular import get_top_pid_info


logger = use_logger()
pdc = ProductDataClass()
product_list = []


def run_init(need_init_job=True):
    if need_init_job:
        try:
            stop_dicom_service()
            # rm_rabbitmq()
            rm_alg_job()
            rm_dicom()
            rm_redis()
            rm_product()
            rm_cases()
            rm_logs()
            start_dicom_service()
            # 开启显卡高性能模式
            start_nvidia_pm()
        except Exception as e:
            logger.info(str(e))
            run_init(need_init_job)
    logger.info(" init job success ")


def worklist():
    product_workspace = config.PRODUCTS_WORKSPACE
    for p in os.listdir(product_workspace):
        _product = os.path.join(product_workspace, p)
        if os.path.isdir(_product):
            product_list.append(_product)
    logger.info(product_list)
    products = list(set(product_list))
    return products


def wait_(func):
    def wait(ctime=0):
        func(ctime)
        if ctime == 0:
            return
        time.sleep(ctime)
        return
    return wait


def push(work_list, product, j):
    """
    :param work_list:
    :param product:
    :param j
    :return:
    """
    server_ip = '10.10.10.91'
    server_port = 11112
    press_num = j['press_num']
    ctime = j['press_rate']
    delay = j['delay']
    loss = j['loss']
    calculate_dict = {}

    if delay == 0 and loss == 0:
        cmd = ''
    elif delay != 0 and loss == 0:
        cmd = f'echo "j75yHMC8n2:"| sudo -S tc qdisc add dev ens11f0 root netem delay {delay}ms'
    elif delay == 0 and loss != 0:
        cmd = f'echo "j75yHMC8n2"| sudo -S tc qdisc add dev ens11f0 root netem loss {loss}%'
    else:
        cmd = f'echo "j75yHMC8n2"| sudo -S tc qdisc add dev ens11f0 root netem delay {delay}ms loss {loss}%'

    exec_cmd('echo "j75yHMC8n2"| sudo -S tc qdisc del dev ens11f0 root netem')
    p = PushFrom('10.10.10.77', '22', 'devops1', 'P3CkvtrBxn')
    p.do_cmd('echo "P3CkvtrBxn"| sudo -S tc qdisc del dev ens11f0 root netem')

    # 修改dicom元信息
    def change_dicom():
        change_dicom_meta(config.PRODUCTS_WORKSPACE, str(j['num']), product)

    def push_list():
        push_client = StoreScu(
            aec='SKDICOMINT91',
            aet=f'{product}_script',
            server_ip=server_ip,
            server_port=server_port,
        )

        to_do = []

        time.sleep(30)
        while True:
            workers = work_list[0:press_num] if len(work_list) >= press_num else work_list
            with futures.ThreadPoolExecutor(max_workers=10) as executor:
                for w_path in workers:
                    cal_path = w_path.split('/')[-1]
                    logger.info(f"push {w_path}")
                    f = executor.submit(push_client.push, w_path)
                    calculate_dict[cal_path + '_start'] = str(datetime.datetime.now())
                    to_do.append(f)
            for future in to_do:
                if future.done():
                    if calculate_dict.get(cal_path+'_end'):
                        continue
                    else:
                        calculate_dict[cal_path+'_end'] = str(datetime.datetime.now())

            logger.info(f"calculate_dict: {calculate_dict}")
            if len(work_list) >= press_num:
                del work_list[0: press_num]
            else:
                del work_list[0: len(workers)]

            if not ctime == 0:
                logger.info(f"time sleep {ctime*60}")
                time.sleep(ctime*60)

            if len(work_list) == 0:
                break

    if product != 'products':
        change_dicom()

    if j['push_from'] == 91:
        exec_cmd(cmd)
        push_list()
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'calculate.log'), 'w+') as cal_file:
            cal_file.write(json.dumps(calculate_dict))
        exec_cmd('echo "j75yHMC8n2"| sudo -S tc qdisc del dev ens11f0 root netem')

    else:
        p.sftp_file()
        p.do_cmd(cmd)
        p.do_push(press_num, ctime)
        p.do_cmd('echo "P3CkvtrBxn"| sudo -S tc qdisc del dev ens11f0 root netem')
        p.ssh_close()

    while True:
        time.sleep(5)
        if not pdc.check_case_completed(pdc.coronary_session, pdc.coronary_cases):
            logger.info("coronary case not completed waiting...")
            continue
        elif not pdc.check_case_completed(pdc.cerebral_session, pdc.cerebral_cases):
            logger.info("cerebral case not completed waiting...")
            continue
        elif not pdc.check_case_completed(pdc.calcium_session, pdc.calcium_cases):
            logger.info("calcium case not completed waiting...")
            continue
        elif not pdc.check_case_completed(pdc.thoracic_session, pdc.thoracic_cases):
            logger.info("thoracic case not completed waiting...")
            continue
        else:
            break


def run_press(product=None):
    p_json = dict()
    p_json['num'] = int(os.getenv('num', 100))
    p_json['need_init_job'] = os.getenv('need_init_job', False)
    p_json['press_type'] = os.getenv('press_type', 'once')
    p_json['press_num'] = int(os.getenv("press_num", 10))
    p_json['press_rate'] = int(os.getenv('press_rate', 0))
    p_json['push_from'] = int(os.getenv('push_from', 91))
    p_json['delay'] = int(os.getenv('delay', 0))
    p_json['loss'] = int(os.getenv('loss', 0))

    logger.info(f"key: {p_json}")
    get_top_pid_info()

    while True:
        run_init(p_json['need_init_job'])
        plist = worklist()
        push(plist, product, p_json)
        try:
            products_assert()
            calculate_alg()
        except Exception as e:
            logger.info(e)
            break
        if p_json['press_type'] == 'once':
            break
        else:
            abs_path = os.path.dirname(os.path.abspath(__file__))
            if os.path.exists(os.path.join(abs_path, 'logs', 'sign')):
                break
        p_json['num'] += p_json['num']
