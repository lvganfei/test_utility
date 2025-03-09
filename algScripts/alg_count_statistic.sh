#! /bin/bash
# ------用法------
# 将此脚本复制到服务器/data1/data/output目录中，运行sh collect_alg_log.sh coronary/cerebral/thoracic， 参数为文件夹名称
# ---------------
count=0
total=`ls -l $1 | grep "^d" | wc -l`

for case in `ls $1`
do
  echo $case
  if [ ! -d $1/$case ];then
    echo 'skip file'
    continue
  fi
  cat $1/$case/cerebral.log | grep 'Alg version'
  result=`cat $1/$case/cerebral.log | grep 'All Completed'`
  echo $result
  if [ ! "$result" = "" ];then
    echo 'pass'
    ((count++))
  fi
  #echo $case >> cerebral_time.txt
  #cat $1/$case/cerebral.log | grep Finished
done

echo "total $total cases"
echo "success cases: $count"