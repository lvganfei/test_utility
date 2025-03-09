#! /bin/sh
# 前提条件，先创建failedcase.log保存所有失败的case_num到/data1/data/output/coronary,格式如下：
# root@master:/data1/data/output/coronary# cat failedcase.log  
# T20200317095321Hdf71a951d7b9b239
# T20200317095414H5630fccc77f7cc52
# T20200317095330H0c4ff472fa5119c1

# 然后搜集log到logDir文件夹下，最后压缩
today=`date +'%Y-%m-%d'`

mkdir "failed-log-$today"
for case in `cat $3 | awk '{print $1}'`
  do
    echo /data1/data/output/$1/$case
    if [ ! -f /data1/data/output/$1/$case/$2.log ];then
      echo 'no cta.log'
      continue
    fi
    cp -f /data1/data/output/$1/$case/$2.log failed-log-$today/$case.log
  done
# 压缩为一个tar包
tar -zcvf failed-log-$1-$today.tar.gz failed-log-$today