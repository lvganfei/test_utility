import os
import logging
from sk_common.log_handlers import init_logger
from dataclasses import dataclass


@dataclass
class Config:
    HOST: str = '10.10.10.91'
    DB_PORT: str = '13306'
    MONGO_PORT: str = '17017'
    CSV_FILE: str = "report.csv"
    SYS_CSV_FILE: str = "sys_report.csv"
    TEST_OUTPUT: str = "/test/test_output/P38T20190929153113R431"
    DICOM_ORIGIN: str = "/data1/data/original"
    DICOM_URI: str = f"mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@{HOST}:{DB_PORT}/plt_dicom?charset=utf8mb4"
    CORONARY_URI: str = f"mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@{HOST}:{DB_PORT}" \
        f"/plt_coronary?charset=utf8mb4"
    CORONARY_MONGO_URI: str = f"mongodb://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@{HOST}:{MONGO_PORT}/plt_coronary"
    CORONARY_WORKSPACE: str = "/test_data/platform-test/press_data/source/coronary"
    CORONARY_OUTPUT: str = "/data1/data/output/coronary"
    CORONARY_SOURCE: str = "/data1/data/source/coronary"
    CALCIUM_URI: str = f"mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@{HOST}:{DB_PORT}" \
        f"/plt_calcium?charset=utf8mb4"
    CALCIUM_MONGO_URI: str = f"mongodb://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@{HOST}:{MONGO_PORT}/plt_calcium"
    CALCIUM_WORKSPACE: str = "/test_data/platform-test/press_data/source/calcium"
    CALCIUM_OUTPUT: str = "/data1/data/output/calcium"
    CALCIUM_SOURCE: str = "/data1/data/source/calcium"
    CEREBRAL_URI: str = f"mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@{HOST}:{DB_PORT}" \
        f"/plt_cerebral?charset=utf8mb4"
    CEREBRAL_MONGO_URI: str = f"mongodb://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@{HOST}:{MONGO_PORT}/plt_cerebral"
    CEREBRAL_WORKSPACE: str = "/test_data/platform-test/press_data/source/cerebral"
    CEREBRAL_OUTPUT: str = "/data1/data/output/cerebral"
    CEREBRAL_SOURCE: str = "/data1/data/source/cerebral"
    THORACIC_URI: str = f"mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@{HOST}:{DB_PORT}" \
        f"/plt_thoracic?charset=utf8mb4"
    THORACIC_MONGO_URI: str = f"mongodb://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@{HOST}:{MONGO_PORT}/plt_thoracic"
    THORACIC_WORKSPACE: str = "/test_data/platform-test/press_data/source/thoracic"
    THORACIC_OUTPUT: str = "/data1/data/output/thoracic"
    THORACIC_SOURCE: str = "/data1/data/source/thoracic"
    PRODUCTS_WORKSPACE: str = "/data1/test/platform-test/press_data/source/products"
    PRODUCTS_OUTPUT: str = '/data1/data/output'
    REDIS_WORKSPACE: str = "/data1/redis"
    RABBIT_WORKSPACE: str = "/data1/rabbitmq"


def use_logger():
    logger = logging.getLogger(__name__)
    init_logger(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.ini'))
    return logger


config = Config()


