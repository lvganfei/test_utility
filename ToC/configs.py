import os
import logging
from dataclasses import dataclass


@dataclass()
class Config(object):
    MYSQL_URL: str = ''


def singleton(cls):

    _instance = dict()

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return _singleton


@singleton
def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    debug_log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'debug.log')
    log_format = logging.Formatter('%(asctime)s-%(name)s-%(filename)s-'
                                   '[line:%(lineno)d]-%(levelname)s-[日志信息]: %(message)s',
                                   datefmt='%a, %d %b %Y %H:%M:%S')

    fh = logging.FileHandler(debug_log_path, mode='a+', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(log_format)
    logger.addHandler(fh)

    return logger


config = Config()
