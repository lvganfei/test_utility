from apscheduler.schedulers.background import BackgroundScheduler
from press.conf import use_logger
import subprocess
import sys
import time
import requests


logger = use_logger()
error_warning = []


def get_top_pid_info():
    command = "top -bn 1 -i -c|awk '{if (NR > 6) print}'|awk '{if ($9 > 70) print}'"
    logger.info(sys.platform)
    if not sys.platform == 'linux':
        logger.info(" just support for linux-ubuntu")
    response = subprocess.getoutput(command)
    logger.info('\n' + str(response))
    for r in response.split('\n'):
        if r in error_warning:
            continue
        error_warning.append(r)
        logger.info("add sk information")
        post_msg(r)


def run():
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_top_pid_info, 'interval', seconds=5)
    try:
        scheduler.start()
        while True:
            time.sleep(1)
    except(KeyboardInterrupt, SystemExit):
        logger.info("scheduler shutdown")
        scheduler.shutdown()


def post_msg(content):
    return requests.post(
        url='http://109.244.38.204:19292/api/v1/send', json=
        {
            "content": content,
            "recipients": [
                {
                    "recipient": "TESTOR_GROUP",
                    "type": 0
                }
            ],
            "sendWays": [
                1
            ],
            "title": "91压测cpu使用率高于70%的进程信息",
        }
    )


if __name__ == '__main__':
    get_top_pid_info()
