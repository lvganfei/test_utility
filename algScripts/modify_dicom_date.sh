# /bin/bash
# 批量修改一个文件夹中的病人姓名
for instid in `ls $1`
do
  echo $instid
  if [ ! -d $1/$instid ];then
    continue
  fi
  case=`echo $instid | awk -F '.' '{print $1}'`
  echo $case
  dcmodify -v -ma "(0008,0020)=20200511" $1/$instid/slices/
  dcmodify -v -ma "(0008,0021)=20200511" $1/$instid/slices/
#中台数据已脱敏，病人姓名和病例号会变成随机字符。为了方便测试需要对数据进行反脱敏，把病例号改成方便查询的字符
  rm -f $1/$case/slices/*.dcm.bak
  #storescu -v -aec SKDICOMINT -aet algtest 109.244.38.201 31112 +sd $1/$case/slices/

done
