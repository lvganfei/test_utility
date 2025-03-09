import re

path = '/Users/jp/fsdownload'
All_Ram = []
All_I = []
All_O = []

with open(path + '/zhangyuexian_1s1cuda11.log', 'r') as cont:
    t = cont.readlines()
    for i in t:
        # 截取所有需要的数据
        all_content = re.search(
            r'.*%\s+(.*?) / (.*?[GiB|MB|kB|GB|B|MiB])\s+(.*?)%\s+(.*?[GiB|MB|kB|GB|B|MiB]) / (.*?[GiB|MB|kB|GB|B|MiB])\s+(.*?[GiB|MB|kB|GB|B|MiB]) / (.*?[GiB|MB|kB|GB|B|MiB])\s+.*',
            i)
        if all_content is not None:
            All_Ram.append(all_content.group(1))
            All_I.append(all_content.group(6))
            All_O.append(all_content.group(7))


# 获取最大内存
def get_max_ram():
    gib = []
    # 判断内存是GiB还是MiB
    for a in All_Ram:
        result_dw = ''.join(re.findall(r'[a-zA-Z]*', a))
        result_sz = ''.join(re.findall(r'[0-9]*[\.|0-9][0-9]*', a))
        if result_dw == 'GiB':
            gib.append(float(result_sz))
    max_ram = gib[0]
    for b in range(1, len(gib)):
        if max_ram < gib[b]:
            max_ram = gib[b]
    print('最大内存为:', max_ram, 'GiB')


# 区分GB、MB、kB,统一返回kB
def unit(x):
    gb = []
    mb = []
    kb = []
    for c in x:
        result_dw = ''.join(re.findall(r'[a-zA-Z]*', c))
        result_sz = float(''.join(re.findall(r'[0-9]*[\.|0-9][0-9]*', c)))
        if result_dw == "GB":
            gb_kb = result_sz * pow(1024, 2)
            gb.append(gb_kb)
        elif result_dw == "MB":
            mb_kb = result_sz * 1024
            mb.append(mb_kb)
        elif result_dw == "kB":
            kb.append(float(result_sz))
    if gb:
        return gb
    elif mb:
        return mb
    else:
        return kb


# 获取io的最大值
def get_max_io(x, y):
    gb_io = unit(x)
    max_io = gb_io[0]
    for d in range(1, len(gb_io)):
        if max_io < gb_io[d]:
            max_io = gb_io[d]
    print('最大', y, '为:', max_io, 'kB')


if __name__ == '__main__':
    get_max_ram()
    get_max_io(All_I, 'I')
    get_max_io(All_O, 'O')
