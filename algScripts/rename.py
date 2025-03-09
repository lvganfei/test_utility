import sys
def rename_null(pth):
    import os
    import sys
    pth = sys.argv[1]
    dir_lst = os.listdir(pth)
    for dr in dir_lst:
        ndr1 = dr.replace(' ', '\ ')
        ndr2 = dr.replace(' ', '_')
        pt1 = os.path.join(pth, ndr1)
        pt2 = os.path.join(pth, ndr2)
        cmd = 'mv ' + pt1 + ' ' + pt2
        print(cmd)
        os.system(cmd)
if __name__ == '__main__':
    pth = sys.argv[1]
    rename_null(pth)
