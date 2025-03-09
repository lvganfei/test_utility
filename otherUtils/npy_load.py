# 进入/data1/data/source/coronary/$case_num/目录,运行方式python3 npy_load.py 10
import numpy as np
import time
import os
import sys

print(sys.argv)
print(np.__version__)
load_time=[]
cmd1 = 'sync'
cmd2 = 'echo 3 > /proc/sys/vm/drop_caches'

def f(l):
  #t = time.time()
  for i in range(l):
    print(i)
    os.system(cmd1)
    os.system(cmd2)
    t = time.time()
    np.load('myo_dist.npy')
    load_time_single=time.time() - t
    print(load_time_single)
    load_time.append(load_time_single)
    # t = time.time()
  
  print(load_time)
  print(np.mean(load_time))

if __name__ == "__main__":
  f(int(sys.argv[1]))