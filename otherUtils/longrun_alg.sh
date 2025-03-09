#!/usr/bin/env bash
# 每隔十分钟获取alg-jon镜像，如果没有则重新分发计算
while true
do
    algjobs=`docker ps | grep alg-job`
    if [[ -z $algjobs ]]; then
        echo 'no alg-job, apply coronary, cerebral, thoracic again'
        
        python3 apply_all_rondomly.py 127.0.0.1

        echo 'sleep 200s and apply ctp'
        
        sleep 200
        
        python3 apply_ctp_local.py 127.0.0.1 ctp_200_patient_series.json
        
        echo 'apply finish, sleep 4 hours'
        sleep 60*60*4
    else
        echo 'alg-job exists, wait 5m again'
        sleep 300
    fi
done