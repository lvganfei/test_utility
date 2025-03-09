import torch
import os
import sys

if __name__ == '__main__':
    root = sys.argv[1]
    print(root)
    with open(root, 'r') as fin:
        file_list = fin.readlines()
        fin.close()

    # for root, dirs, files in os.walk(root, topdown=False):
    for name in file_list:
        if name.find('pkl') > -1:
            # print(name)
            try:
                torch.load(os.path.join(root,name))
                print(f'load {name} pkl successfully?')
            except Exception as e:
                print(f'{os.path.join(root,name)} pkl encypt')
        elif name.find('jit') > -1:
            # print(name)
            try:
                torch.jit.load(os.path.join(root,name))
                print(f'{os.path.join(root,name)} load jit successfully?')
            except Exception as e:
                print(f'{name} jit encypt')