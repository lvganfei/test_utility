import time
import os
import sys
import subprocess
import json
from sk_dicom_interface.storescu import StoreScu


default_num = int(sys.argv[1])
ctime = int(sys.argv[2])


def internet_fitter(command):
    for cmd in command:
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


def push_list():
    if os.path.exists('/home/democompany/script/progress.json'):
        os.remove('/home/democompany/script/progress.json')
    server_ip = '10.10.10.91'
    server_port = 11112
    work_space = "/data1/test/platform-test/press_data/source/products"
    work_list = os.listdir(work_space)

    push_client = StoreScu(
        aec='SKDICOMINT',
        aet='77-products-script',
        server_ip=server_ip,
        server_port=server_port,
    )

    while True:
        workers = work_list[0:default_num] if len(work_list) >= default_num else work_list
        try:
            for w_path in workers:
                with open('/home/democompany/script/progress.json', 'w+') as f:
                    f.write(json.dumps({"progress": "push {}".format(w_path)}))
                print(os.path.join(work_space, w_path))
                push_client.push(os.path.join(work_space, w_path))

            if len(work_list) >= default_num:
                del work_list[0: default_num]
            else:
                del work_list[0: len(workers)]

            if not ctime == 0:
                print("time sleep {}".format(ctime * 60))
                time.sleep(ctime * 60)

            if len(work_list) == 0:
                break
        except Exception as e:
            with open('/home/democompany/script/progress.json', 'w+') as f:
                f.write(json.dumps({"progress": "error: {}".format(str(e))}))
            break

    with open('/home/democompany/script/progress.json', 'w+')as f:
        f.write(json.dumps({"progress": "done"}))


if __name__ == '__main__':
    push_list()
