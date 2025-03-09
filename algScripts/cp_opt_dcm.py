import os
import sys
from datetime import datetime 
###read txt getID###
lpath = '/data0/cerebral/liutao/liutao/caseID.txt'
f = open(lpath,"r")
lines = f.readlines()

idlst = []
for i in range(len(lines)):
    pth = lines[i].split('\n')[0]

#     pth = pth.split(':')[-1]
#     pth = pth.split(' ')[-1]
    path = pth.split(' ')[-1]
    
    idlst.append(path)
print(idlst)
#####make time dir####
putpath = '/data0/cerebral/liutao/liutao/'
day_time = datetime.now().strftime('%Y-%m-%d')
print(day_time)
# pwd = os.getcwd()+day_time
# print(pwd)
newpath = putpath+'yy_output'+day_time
if not os.path.exists(newpath):
    os.makedirs(newpath)
print('outputpath: ', newpath)
newpath1 = putpath+'yy_dcm'+day_time
if not os.path.exists(newpath1):
    os.makedirs(newpath1)
print('dcmpath: ', newpath1)

####cp output files###
path3 = '/data1/data/output/cerebral'
for f in idlst:
    path2 = os.path.join('/data1/data/source/cerebral',f+'/')
for i in idlst:
    datapath = os.path.join(path, i+'/')
    outputpath = os.path.join(newpath, i+'/')
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)
    print('outputpath: ',outputpath)
for f in idlst:
    log = os.path.join(path3,f,'cerebral.log')
    graph_json = os.path.join(path3, f, f+'_graph.json')
    ranges_json = os.path.join(path3, f, 'ranges.json')
    npy = os.path.join(path3, f, '*.npy')
    npz = os.path.join(path3, f, '*.npz')
    naming_secs = os.path.join(path3, f, 'naming_secs.json')
    naming = os.path.join(path3, f, 'naming')
    slices = os.path.join(path3, f, 'slices')
    vr = os.path.join(path3, f, 'vr')
    vr_mask = os.path.join(path3, f, 'vr_mask')
    cmd1 = 'cp '+ log + ' '+ os.path.join(newpath , f+'/')
    cmd2 = 'cp '+ graph_json + ' '+ os.path.join(newpath , f+'/')
    cmd3 = 'cp '+ ranges_json + ' '+ os.path.join(newpath , f+'/')
    cmd4 = 'cp '+ npy + ' '+ os.path.join(newpath , f+'/')
    cmd5 = 'cp '+ npz + ' '+ os.path.join(newpath , f+'/')
    cmd6 = 'cp -r '+ naming + ' '+ os.path.join(newpath , f+'/')
    cmd7 = 'cp -r '+ slices + ' '+ os.path.join(newpath , f+'/')
    cmd8 = 'cp '+ naming_secs + ' '+ os.path.join(newpath , f+'/')
    cmd9 = 'cp -r '+ vr + ' '+ os.path.join(newpath , f+'/') 
    cmd10 = 'cp -r '+ vr_mask + ' '+ os.path.join(newpath , f+'/')
    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)
    os.system(cmd4)
    os.system(cmd5)
    os.system(cmd6)
    os.system(cmd7)
    os.system(cmd8)
    os.system(cmd9)
    os.system(cmd10)
####cp dcm data
for filename1 in idlst:
    original = os.path.join('/data1/data/source/cerebral/', filename1+'/')
    output2 = os.path.join(newpath1, filename1+'/')
    if not os.path.exists(output2):
        os.makedirs(output2)
    print('dcmpath: ',output2)
    all_slicesname1 = [f.split('.dcm')[0] for f in os.listdir(original) if f.endswith('.dcm')]
    for slicename1 in all_slicesname1:
        cmd_dcm = 'cp '+ original+ slicename1+ '.dcm '+ output2+ slicename1+ '.dcm'
        os.system(cmd_dcm)
tar = 'tar -zcf '+ newpath + '.tar.gz'+' '+ 'yy_output'+day_time
#tar1 = 'tar -zcf '+ newpath1+'.tar.gz' +' '+ 'yy_dcm'+day_time
os.system(tar)
#os.system(tar1)
