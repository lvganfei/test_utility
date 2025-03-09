#!/usr/bin/env bash

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
    echo 'case_num'|tr "\n" "," > calculate.csv
    cat $1/$case/cerebral.log|grep -e Finished|awk -F 'Finished' '{print $2}'|awk -F 's\.' '{print $1}'|awk -F ' in' '{print $1}'|tr "\n" ',' >>calculate.csv
    echo '\n' >> calculate.csv
  fi
done

for case in `ls $1`
do
  echo $case
  if [ ! -d $1/$case ];then
    echo 'skip file'
    continue
  fi
  echo $case|tr "\n" "," >> calculate.csv
  cat $1/$case/cerebral.log|grep -e Finished|awk -F 'Finished' '{print $2}'|awk -F 's\.' '{print $1}'|awk -F ' in' '{print $2}'|sed 's/ //g'|tr "\n" "," >> calculate.csv
  echo '\n' >> calculate.csv
done

cat calculate.csv