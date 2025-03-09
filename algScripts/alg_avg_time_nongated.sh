#! /bin/bash
# 搜集指定的case计算时间并计算平均值，输入子产品名，log文件和case_num列表的路径。例如 bash avg_time.sh coronary cta case_list.log
folder="/data1/data/output/$1"
sum=0
count=0
today=`date +'%Y-%m-%d'`
echo "case_num,version,total_time" >> alg_time_$1_$today.csv

for i in `ls $folder`
do
  if [ -f "$folder/$i/$2.log" ];
  then
    version=`cat "$folder/$i/$2.log" | grep 'Alg version:' | awk '{print $3}'`
    ltime=`cat "$folder/$i/$2.log" | grep 'cct_cal finish' | awk '{print $4}'`
    if [[ -n "$ltime" ]] && [[ -n "$version" ]];
    then
  
      echo -ne "\n$i,$version,$ltime" >> alg_time_$1_$today.csv
      oldifs="$IFS"
      IFS=$'\n'
      for component in `cat "$folder/$i/$2.log" | grep 'time:' | awk -F 'time: ' '{print $2}'`
        do
          component_time=`echo $component | awk '{print $NF}'`
          echo -n ",$component_time" >> alg_time_$1_$today.csv
        done
      IFS="$oldifs"
      sum=`echo "$sum+$ltime" | bc`
      echo $ltime
      # echo -e "\n" >> alg_time_$1.csv
      ((count=$count+1))

    else
      echo "case $i failed"
      echo "$i" >> faliedcase_$1_$today.log
    fi
  else
    echo "case $i no log file"
  fi
done
echo "总数: $count"
avg=`echo "$sum/$count" | bc`
echo "average time: $avg"
echo "average,$avg" >> alg_time_$1_$today.csv