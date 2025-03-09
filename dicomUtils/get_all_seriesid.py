import subprocess
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_JOB_EXECUTED
from concurrent.futures import ProcessPoolExecutor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from hashlib import md5
import logging
import time
import pydicom
import os


logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sqlurl = "mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@10.12.10.77:13306/universe_test?charset=utf8mb4"

class DBModel(object):

    def __init__(self, url):
        # 创建数据库引擎
        engine = create_engine(url, echo=False, encoding='utf-8', pool_size=20, pool_recycle=300)

        # 创建数据模型绑定
        Base = automap_base()
        Base.prepare(engine, reflect=True)

        # 通过Base获取表属性
        self.Push_Statistics = Base.classes.push_statistics

        # 创建session 绑定数据库, 查询方式建议用with
        sessionClass = sessionmaker(bind=engine)
        self.session = sessionClass()

def storescu(list=[]):
    #数据库初始化
    # engine = create_engine(sqlurl, echo=False, encoding='utf-8', pool_size=50, pool_recycle=300)

    db_instance = DBModel(sqlurl)
    session = db_instance.session
    Push_Statistics =  db_instance.Push_Statistics

    suffix = md5(str(list).encode('utf-8')).hexdigest()
    # total_count_path = os.path.join(os.getcwd(), 'count_' + suffix + '.pcount')

    
    result = {}

    #从环境变量中获取节点等信息
    # ae = os.getenv('DESTINATION_AE')
    # ip = os.getenv('DESTINATION_IP')
    # base_dir = '/data1/universe-longrun-data/coronary'
    interval = '1'
    for i in range(len(list)):
        path = list[i]["folder_name"]
        series_instance_uid = list[i]["series_instance_uid"]

        starttime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        result[path] = {"id":i, "series_instance_uid":series_instance_uid, "start_time": starttime, "end_time":"", "result":""}
       

        # command = 'storescu -xs -aec ' +ae+' -aet jenkins-parallel ' + ip + ' 11112 +sp *.dcm +sd +r ' + base_dir + '/' + path
        # _p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # _p.wait()
        # time.sleep(int(interval))
        finishtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        
        
        result[path]["end_time"] = finishtime
        result[path]["result"] = 'success'
        record = Push_Statistics(series_instance_uid = series_instance_uid, start_time = starttime, finish_time=finishtime, result = 'success')
        session.add(record)
        session.commit()
        
        
        logger.info(path + ' 目录推送完成')
        
    
    logger.info('当前进程序列全部推送完成')

    return result


def get_total_count():
    file_list = os.listdir(os.getcwd())
    total_count = 0
    for f in file_list:
        if f.find('.pcount') > 0:
            with open(f, 'r') as pcount_file:
                total_count += len(pcount_file.read())
                pcount_file.close()
    return total_count


def notify():
    old_count_path = os.path.join(os.getcwd(), 'last_hour.lcount')

    with open(old_count_path, 'r') as old_count_file:
        old_count = int(old_count_file.read())
        old_count_file.close()

    total_count = get_total_count()
    count_h = total_count - old_count
    
    with open(old_count_path, 'w') as old_count_file:
        old_count_file.write(str(total_count))
        old_count_file.close()


    receiver = os.getenv('MAIL_RECEIVER')
    service = os.getenv('service')
    command = 'python3 /data1/press-test-data/jenkins_scripts/mail_notification_jenkins_interval.py ' + str(total_count) + ' '+ str(count_h) + ' ' + service + ' '+ receiver   
    _p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    _p.wait()
    if (_p.returncode == 0):
            logger.info('邮件发送成功')
    else:
        logger.error(_p.stderr.read())
        logger.error('邮件发送失败')

def run_parallel():
    '''
    通过jenkins设置以下环境变量，并通过os模块获取
    SOURCE_DIR
    DESTINATION_IP
    DESTINATION_AE
    service
    PUSH_INTERVAL
    '''
    
    
    # 环境变量，记录总推送数量和当前小时推送数量

    dicom_source = '/data1/universe-longrun-data/coronary'
    count = '3'
    logger.info('并发数: ' + count)
    # logger.info(count)
    #将推送目录的文件夹平均分成count份，先去掉非文件夹
    if count != None:
        count = int(count)
    source_list = os.listdir(dicom_source)
    # logger.info(source_list)
    # logger.info(len(source_list))
    folder_list = []
    for i in source_list:
        # 只处理文件夹
        if (os.path.isdir(os.path.join(dicom_source, i))):
            logger.info('++++++++++++++++++++++++++++dir+++++++++++++++++')
            series_instance_uid = ''
            # 寻找dcm文件并获取series_instance_uid
            logger.info('正在寻找dcm文件并获取series_instance_uid')
            # for root, dirs, files in os.walk(os.path.join(dicom_source, i), topdown=True, onerror=None, followlinks=False):
            #     for file in files:
                    
            #         if file.find('.dcm') != -1:
            #             logger.info(file)
            #             ds = pydicom.dcmread(os.path.join(root, file), force=True)
            #             series_instance_uid = ds.SeriesInstanceUID
            #             logger.info(series_instance_uid)
            #             break
            folder_list.append({"folder_name": i, "series_instance_uid": i})
        
    logger.info('所有文件夹和seriese instance uid 列表')
    logger.info(folder_list)
    dicom_list_len = len(folder_list)

    # 算出每批原片列表的数量
    slice_len = dicom_list_len//count

    logger.info('total folder list: ' + str(dicom_list_len))
    # logger.info('每份序列list长度: ' + str(slice_len))
    
    #将总的列表拆成count份
    all_slice = []
    for i in range(count):
        # logger.info('index: '+ str(i))
        # logger.info(i*slice_len)
        # logger.info((i+1)*slice_len)

        # 最后的列表包含所有剩余的项目
        if (i == count - 1):
            all_slice.append(folder_list[i*slice_len:])
        else:
            all_slice.append(folder_list[i*slice_len:(i+1)*slice_len])
    
    logger.info('拆分后的序列，每份序列list长度: ' + str(slice_len))
    logger.info(all_slice)
    # for a in range(len(all_slice)):
    #     logger.info(len(all_slice[a]))


    # 定时通知任务
    # ex_de = ProcessPoolExecutor(max_workers=2)
    # executors = {
    #     'default': ex_de
    # }

    # scheduler = BackgroundScheduler()
    # scheduler.add_job(
    #     notify,
    #     minute=59,
    #     trigger = 'cron'
    # )
    # scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    # scheduler._logger = logging
    # scheduler.start()

    with ProcessPoolExecutor(max_workers=count) as executor:
        futures = executor.map(storescu, all_slice)
        # logger.info(futures)
        for future in futures:
            logger.info(future)
            logger.info(len(future))
    





if __name__ == '__main__':
    logger.info('推送开始时间')
    logger.info(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
    run_parallel()
    logger.info('推送结束时间')
    logger.info(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
    