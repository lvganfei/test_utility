#!/bin/bash
echo "开始等待服务$1 变更完成"
count=0
while true
do 
result=$(kubectl -n test-pr get pods -l platform=$1 | tail -n 1 | awk '{print $3}')
podname=$(kubectl -n test-pr get pods -l platform=$1 | tail -n 1 | awk '{print $1}')
echo "kubectl -n test-pr get pods -l platform=$1"
 if [[ $result =~ "Terminating" || $result =~ "ContainerCreating" || $result =~ "CrashLoopBackOff" ]];
 then
    echo $podname
    echo $result
    echo 'sleep 3s'
    ((count=$count+1))
    sleep 3
    if [ $count =gt 10 ]
        then 
            echo "kill $podname"
            kubectl delete pod $podname -n test-pr --force —grace-period=0
            break
        fi
 elif [[ $result =~ "InvalidImageName" ]];
 then
    echo 'invalid image name, exit'
    exit 1
 else
    echo $result
    echo "change finish"
    break;
 fi
done