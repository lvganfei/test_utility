#!/bin/bash
#for coronary
root_dir=$1
find_result=`find $root_dir -mmin -20 -type d`
echo $find_result
if [ -n "$find_result" ];
then
 for casenum in $find_result
   do
    echo "push $casenum to new platform"
    storescu -v -aec SKDICOMINT2 -aet oldplt 10.0.61.136 11112 +sd +r +sp *.dcm
   done
else
  echo 'no new case'
fi

