#! /bin/bash
# push dicom via storescu ip port path
# example bash push_dicom_period.sh SKDICOMINT 11112 /data1/platform-test/data/source/coronary
# Cardiac/Coronary
# /data1/platform-test/data/source/coronary/
echo $1
echo $2
echo $3
for case in `ls $3`;
    do  
        dir_or_file=$3"/"$case
        if [ -d $dir_or_file ]
        then
            echo "$1/$case is a dir"
            storescu -v -aec SKDICOMINT124 -aet script $1 $2 +sd $3"/"$case/
            echo 'finish scu and sleep 60s'
            sleep 30s
            echo 'deal with another case'
        else
            # echo $dir_or_file
            echo  "$dir_or_file is a file"
        fi
    done

echo 'all finished'

