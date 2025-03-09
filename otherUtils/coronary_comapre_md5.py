#!/usr/bin/env python
# coding: utf-8

# In[12]:


import os
import sys
import csv
import subprocess
import numpy as np
import hashlib


# In[23]:


def get_md5sum():

    casenums = ['T20200829230426H7fc663be','T20200829230426H2bacdf76','T20200829230426H363b8467','T20200829230426H5d7d7e1e',
                'T20200829230426Hb0f8955a','T20200829230426H5b92ea06','T20200829230217H9d9d5648','T20200829230426H9f2c2ffc',
                'T20200829231034H60f15679','T20200829230426Had162d54',
               ]

    opt_dir = '/data1/data/output/coronary/'

    if len(sys.argv) > 3:
        print(sys.argv)
        path = sys.argv[1]
        print(path)

    case = []
    files = ['case.npy',
        'myo_mul.npz',
        'shortaxis_seg_dir/tree1_01/tree.npy',
        'straight_dcm/rotate_tree1_01.npy',
        'naming_mapping_txt.json',
        'straight_seg/tree1_01/tree.npy',
        'shortaxis_dcm/tree1_01.npy',
        'narrow_result.json'
        ]

    for casenum in casenums:
        for file in files:
            cmd = 'md5sum {file}'.format(file = os.path.join(opt_dir, casenum, file))
            result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stderr = result.communicate()
            
            '''
            data = '{file}'.format(file = os.path.join(opt_dir, casenum, file))
            md5_value = hashlib.md5(data.encode('utf8')).hexdigest()
            '''
            case.append([casenum, file, result])
    
        with open('./md5sum_test.csv','w') as f:
            csv1 = csv.writer(f)
            csv1.writerows(case)
    print('all complete!')


get_md5sum()
    

    


# In[ ]:




