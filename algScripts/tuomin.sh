# /bin/bash
# 批量解压并修改一个文件夹中的病人姓名
# example: bash tuomin.sh /data1/data/2c918096715ce3ee0172e43badc50542 beijing-youyi
echo $1
echo $2

for instid in `ls $1`
do
  echo $instid
  if [ -d $1/$instid ];then
    echo 'skip folder'
    continue
  fi
  unzip -o -q "$1/$instid" -d "$1/cases"
  case=`echo $instid | awk -F '.' '{print $1}'`
  sleep 1s
  echo $case
  ls $1/cases/$case/slices/*.dcm
  dcmodify -v -ma "(0010,0010)=$2-$case" $1/cases/$case/slices/*.dcm
  dcmodify -v -ma "(0010,0020)=$case" $1/cases/$case/slices/*.dcm

#中台数据已脱敏，病人姓名和病例号会变成随机字符。为了方便测试需要对数据进行反脱敏，把病例号改成方便查询的字
  #storescu -v -aec SKDICOMINT -aet algtest 109.244.38.201 31112 +sd $1/$case/slices/
done
sleep 2s

find $1 -name '*.dcm.bak' -type f | xargs rm -f
