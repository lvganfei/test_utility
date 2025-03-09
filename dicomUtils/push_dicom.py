import re
import logging
import shutil
import time
import os
import sys
import pydicom
import time
import subprocess

from sk_common.log_handlers import init_logger
from sk_dicom_interface.storescu import StoreScu

# logger = logging.getLogger(__name__)
# init_logger('./log.ini')
"""
    推送本地dicom文件到服务器
    用法：
    python push_dicom.py 127.0.0.1 11112 /data/dicom
    
"""

if __name__ == '__main__':
    args=sys.argv
    print(args)
    if len(args) != 4:
        print('参数不对，请输入server地址，端口，和dicom目录, 如python3 push_to_server.py 127.0.0.1 11112 /data/dicom')
    address = args[1]
    port = args[2]
    dicomPath = args[3]
    
    push_client = StoreScu(
        aec = 'SKDICOMINT',
        aet = 'push_script',
        server_ip = address,
        server_port = port,
    )
    push_client.push(dicomPath)
    # cmd = """storescu  -aec SKDICOMINT -aet SKDICOMINT 127.0.0.1 11112 +sd '/data0/rundata/cta_srv_cases/%s/'"""%agr
    # cmd = """storescu  -aec EBM_SERVER168 -aet SKDICOMINT 10.193.7.168 104  +sd '/data0/youyi/%s/'"""%12
    # print cmd
    # print(commands.getoutput(cmd))
    # time.sleep(10)
