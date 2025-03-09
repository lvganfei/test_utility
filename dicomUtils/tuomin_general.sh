# /bin/bash
# 批量解压并修改一个文件夹中的病人姓名
# example: bash tuomin_general.sh /data1/data/2c918096715ce3ee0172e43badc50542
echo $1
count=100
for instid in `ls $1`
do
  echo $instid
  if [ -d $1/$instid ];then
    find $1/$instid -name '*.dcm' -type f | xargs -n1 -I {} dcmodify -v -ma "(0010,0020)=lung-$count" {}
    #find $1/$instid -name '*.dcm' -type f | xargs -n1 -I {} dcmodify -v -ma "(0008,1030)=thoracic" {}
    count=$(($count+1)) 
    sleep 1s
    echo $count
  fi
   echo "$instid finished"
#中台数据已脱敏，病人姓名和病例号会变成随机字符。为了方便测试需要对数据进行反脱敏，把病例号改成方便查询的字
  #storescu -v -aec SKDICOMINT -aet algtest 109.244.38.201 31112 +sd $1/$case/slices/
done

find $1 -name '*.dcm.bak' -type f | xargs rm -f
