# /bin/sh
for case in `ls $1`
do
  echo $case
  if [ ! -d $1/$case ];then
    echo 'skip zip file'
    continue
  fi
  storescu -d -aec SKDICOMINT -aet algtest 10.11.10.137 31112 +sd $1/$case/slices/
  echo 'sleep 10s'
  sleep 10s
done