#!/usr/bin/env bash
# 读取算法时间脚本
# bash cerebral_alg_time.sh /data1/data/output/cerebral

sum=0
for case in `ls $1`
do
  if [ ! -d $1/$case ];then
    echo 'skip file'
    continue
  fi
  num=`cat $1/$case/cerebral.log|grep -e Finished|awk -F 'Finished' '{print $2}'|awk -F 's\.' '{print $1}'|awk -F ' in' 'END {print NR }'`
  echo $num, $sum
  if [ $num > $sum ];then
    sum=$num
    echo $sum
    echo 'case_num'|tr "\n" "," > cerebral_time.csv
    echo 'version'|tr "\n" ","  >> cerebral_time.csv
    cat $1/$case/cerebral.log|grep -e Finished|awk -F 'Finished' '{print $2}'|awk -F 's\.' '{print $1}'|awk -F ' in' '{print $1}'|tr "\n" ',' >>cerebral_time.csv
    echo 'all_completed'|tr "\n" "," >> cerebral_time.csv
    echo '\n' >> cerebral_time.csv
  fi
done

for case in `ls $1`
do
  echo $case
  if [ ! -d $1/$case ];then
    echo 'skip file'
    continue
  fi
  echo $case|tr "\n" "," >> cerebral_time.csv
  cat $1/$case/cerebral.log|grep -e version | head -n 1 | awk -F ':' '{print $2}'|tr "\n" "," >> cerebral_time.csv
  cat $1/$case/cerebral.log|grep -e Finished|awk -F 'Finished' '{print $2}'|awk -F 's\.' '{print $1}'|awk -F ' in' '{print $2}'|sed 's/ //g'|tr "\n" "," >> cerebral_time.csv
  cat $1/$case/cerebral.log|grep -e Completed|awk -F 'Completed' '{print $2}'|awk -F 'in' '{print $2}'|awk '{print substr($0,1,7)}' >> cerebral_time.csv
  # echo '\n' >> cerebral_time.csv
done

cat cerebral_time.csv

echo `date`|tr "\n" ","  > cerebral_Error.txt
echo -e '\n' >> cerebral_Error.txt
for case in `ls $1`
do
  echo $case
  if [ ! -d $1/$case ];then
    echo 'skip file'
    continue
  fi
  all=`cat $1/$case/cerebral.log|grep -e Completed`
  if [ -n "$all" ];then
    echo "True"
  else
    echo "False"
    echo "case_num="$case|tr "\n" "," >> cerebral_Error.txt
    echo -e '\n' >> cerebral_Error.txt
    cat $1/$case/cerebral.log|grep -A 50 "Running failed" >> cerebral_Error.txt
    echo -e '\n\n\n' >> cerebral_Error.txt

  fi
done