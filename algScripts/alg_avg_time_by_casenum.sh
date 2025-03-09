#! /bin/bash
# 搜集指定的case计算时间并计算平均值，输入子产品名，log文件和case_num列表的路径。例如 bash avg_time.sh coronary cta case_list.log
folder="/data1/data/output/$1"
log_name=$2
case_list=$3
sum=0
count=0
today=`date +'%Y-%m-%d'`

# 先取第一个case，获取version, 各模块名称
first_case=`cat ./$case_list | head -n 1`
# echo $first_case
version=`cat "$folder/$first_case/$log_name.log" | grep 'Alg version:' | awk '{print $3}'`
echo $version
component_name=`cat "$folder/$first_case/$log_name.log" | grep 'Finished' | awk -F 'Finished ' '{print $2}' | awk -F ' in ' '{print $1}'| tr -s "\n" ","`
echo $component_name
echo  "case_num,version,total_time,$component_name" >> alg_time_$1_"$version"_"$today".csv
# echo "case_num,version,total_time" >> alg_time_$1_$today.csv

for i in `cat $case_list`
do
  if [ -f "$folder/$i/$log_name.log" ];
  then
    version=`cat "$folder/$i/$log_name.log" | grep 'Alg version:' | awk '{print $3}'`
    ltime=`cat "$folder/$i/$log_name.log" | grep 'All Completed' | awk '{print $4}'`
    if [[ -n "$ltime" ]] && [[ -n "$version" ]];
    then
  
      echo -ne "\n$i,$version,$ltime" >> alg_time_$1_"$version"_"$today".csv
      oldifs="$IFS"
      IFS=$'\n'
      for component in `cat "$folder/$i/$log_name.log" | grep 'Finished' | awk -F 'Finished ' '{print $2}' | awk -F ' in ' '{print $1 $2}' | awk -F ' s. ' '{print $1}'`
        do
          component_time=`echo $component | awk '{print $NF}'`
          echo -n ",$component_time" >> alg_time_$1_"$version"_"$today".csv
        done
      IFS="$oldifs"
      sum=`echo "$sum+$ltime" | bc`
      echo $ltime
      ((count=$count+1))

    else
      echo "case $i failed"
      echo "$i" >> faliedcase_$1_"$version"_"$today".log
    fi
  else
    echo "case $i no log file"
  fi
done
echo $count
avg=`echo "$sum/$count" | bc`
echo "average time $avg"