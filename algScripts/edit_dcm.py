
import pydicom
import os
import re
import traceback
import time
import sys
import argparse
parse = argparse.ArgumentParser()
parse.add_argument('--name', type = str, nargs = '*', help = 'patientName')
parse.add_argument('--path', type = str, nargs = '*', help = 'data path')
# args = parse.parse_args(args=[])
args = parse.parse_args()
names = args.name
pth = args.path
if names is None or pth is None:
    print("ERROR")
    print("you need a patientName or pth")
else:
    print(pth)
    dir_lst = os.listdir(pth[0])
    count = 0
    for f in dir_lst:
        count += 1
        dir_pth = os.path.join(pth[0], f)
        for d in os.listdir(dir_pth):
            dcm_pth = os.path.join(dir_pth, d)
            dcm_info = pydicom.read_file(dcm_pth,force=True)
            pname = dcm_info.PatientName
            pname1 = dcm_info.PatientName = names[0] + '_' + str(pname)
            dcm_info.save_as(dcm_pth)
    print('your patient name : ', names,
         '\nyour data path : ',pth)
