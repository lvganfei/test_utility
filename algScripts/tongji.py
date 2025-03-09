import os
#import cv2
import pydicom
import sys
import numpy as np
import csv
import traceback
path = sys.argv[1]   #####要统计的数的路径 
filename = os.listdir(path)

data = []
l = []
q = []
for name in filename:
    try:
        path1 = os.path.join(path,name)

        d = os.popen('ls '+ path1 +'| shuf -n 1').read()
        n = len(os.listdir(path1))

        path2 = os.path.join(path1,d).split('\n')[0]


        dcm_information = {}
        ds = pydicom.read_file(path2, force=True)

        dcm_information['PatientName'] = ds.PatientName
        dcm_information['PatientID'] = ds.PatientID
        dcm_information['Manufacturer'] = ds.Manufacturer
        dcm_information['InstitutionName'] = ds.InstitutionName
        dcm_information['KVP'] = ds.KVP
        dcm_information['SlicesThinckness'] = ds.SliceThickness
        dcm_information['Version'] = ds.SoftwareVersions
        dcm_information['PatientAge'] = ds.PatientAge
    # ####################    patientid前面会加上   @     ######
        data.append([name
                    ,dcm_information['PatientName']
                    ,'@'+str(dcm_information['PatientID'])
                    ,dcm_information['PatientAge']
                    ,dcm_information['SlicesThinckness']
                    ,dcm_information['KVP']
                    ,dcm_information['InstitutionName']
                    ,dcm_information['Version']
                    ,dcm_information['Manufacturer']
                    ,n])
        if n < 100:
            q.append(name)
    except:

        l.append(name)
#         traceback.print_exc()
print('失败数量: ',len(l),'\nid: \n',l)
print('切片少于100张:',[f for f in q])

def writescv(csvfile, csvheader, csvdata):
    with open(csvfile, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csvheader)
        writer.writerows(csvdata)

csvfile = sys.argv[2] ######csv文件的路径
csvheader = ["casenumber","patientname","Patientid","age","thinckness","KVP","hospital","version","manufacturer","yuanpianshu"]
csvdata = data
writescv(csvfile, csvheader, csvdata)
