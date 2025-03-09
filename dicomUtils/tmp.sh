#! /bin/bash

for case in `cat /data1/log/plt-cerebral-srv/0706failed.log`;
do
    result=`grep 'Completed' /data1/data/output/cerebral/$case/cerebral.log`
    if [[ -n $result ]]
    then
        echo $case
        grep $case /data1/log/plt-cerebral-srv/scheduler.log.2022-07-06
    fi
done