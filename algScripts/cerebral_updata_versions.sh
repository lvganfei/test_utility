#!/usr/bin/env bash
# docker-compose 修改前端断算法版本脚本

if [ $1 == 'srv' ]
then
    cd /home/devops1/sk/product/cerebral
    srv_commit=`cat docker-compose.yaml|grep plt-cerebral-srv:|awk -F ":" '{print $4}'|awk 'NR==2'`
    sed -i "s/$srv_commit/$2/" docker-compose.yaml
    bash stop_cerebral.sh
    bash start_cerebral.sh

elif [ $1 == 'web' ]
then
    cd /home/devops1/sk/product/cerebral
    web_commit=`cat docker-compose.yaml|grep online_|awk -F "_" '{print $2}'`
    sed -i "s/$web_commit/$2/" docker-compose.yaml
    bash stop_cerebral.sh
    bash start_cerebral.sh

elif [ $1 == 'alg' ]
then
    cd /home/devops1/sk/product/platform/workflow
    docker pull storage-shdemocompany:5050/cerebral:$2
    alg_commit=`cat main-prd.yml|grep -A 7 cerebral:|grep alg_version|awk '{print $2}'`
    sed -i "s/$alg_commit/$2/" main-prd.yml
    alg_images_id=`docker ps |grep alg-service | awk '{print $1}'`
    docker restart $alg_images_id
else
    echo "输入错误，请检查输入内容"
fi