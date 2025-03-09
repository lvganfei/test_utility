import sys
pth = sys.argv[1]
aetitle = sys.argv[2]
def post_dcms(path):
    import subprocess
    import os
    import sys

    if len(sys.argv) >= 2:
        path = sys.argv[1]
        print(path)

    dir_list = os.listdir(path)
    for case_num in dir_list:
        dcm_path = os.path.join(path, case_num)
        for dcm in (os.listdir(dcm_path)):
            if os.path.isdir(os.path.join(dcm_path, dcm)) and dcm != 'slices':
                continue
            if 'jpg' in dcm:
                os.remove(os.path.join(dcm_path, dcm))
            if 'slices' in dcm:
                dcm_path1 = dcm_path + '/slices'
                for dcm1 in (os.listdir(dcm_path1)):
                    cmd = "storescu -xs  -aet " + aetitle +  " -aec SKDICOMINT 109.244.38.200  31112  +sd '{path}' ".format(
                        path=os.path.join(dcm_path1, dcm1))
                    print(cmd)
                    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    print(res)
            if 'dcm' in dcm:
                cmd = "storescu  -xs -aet " + aetitle + "  -aec SKDICOMINT 109.244.38.200 31112  +sd '{path}' ".format(
                    path=os.path.join(dcm_path, dcm))
                print(cmd)
                res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                print(res)


post_dcms(pth)

