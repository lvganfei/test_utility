#!/bin/bash


read -p "是否恢复并清理老平台数据Y/N:" ARG


while true ; do
        if [ $ARG == N ] || [ $ARG == Y ];then
                break;
        fi
        read -p "请输入的是否正确参数Y/N:" ARG
        #statements
done

if [[ $ARG == Y ]];then
        echo "数据恢复开始:\n"

        echo "正在清理基础镜像"
        for base_image_id in `docker images | grep 'base' | awk '{print $3}'`
        do
                docker rmi -f $base_image_id
        done

        echo "正在关闭docker 容器"
        for product in `ls /home/devops1/sk/product`
        do
                cd "/home/devops1/sk/product/$product"
                bash stop_"$product".sh
        done

        echo "正在清理6.11镜像"
        for image_id in `docker images | grep '6.11.' | awk '{print $3}'`
        do
                docker rmi -f $image_id
        done

        echo "正在关闭docker 服务"
        systemctl stop docker 

        sleep 30




        if [ -d "/data1/backup/success_test/mongodb" ]; then
                echo "正在清理新平台mongodb"
                rm -rf /data1/mongodb/*
                echo "正在恢复老平台mongodb数据"
                cp -r -v /data1/backup/success_test/mongodb/* /data1/mongodb/
        fi




        if [ -d "/data1/backup/success_test/product" ]; then
                echo "正在清理新平台部署文件"
                rm -rf /home/devops1/sk/product/*
                echo "正在恢复老平台"
                cp -r -v /data1/backup/success_test/product/* /home/devops1/sk/product/
        fi





        if [ -d "/data1/backup/success_test/mysql" ]; then
                echo "正在清理新平台mysql数据"
                rm -rf /data0/mysql/*
                echo "正在恢复老平台mysql数据"
                cp -r -v  /data1/backup/success_test/mysql/* /data0/mysql/
        fi



        echo "正在恢复data数据"

        if [ -d "/data1/backup/success_test/data" ]; then
                echo "正在清理新平台data数据"
                rm -rf /data1/data/*
                echo "正在恢复老平台数据"
                sleep 30
                cp -r -v   /data1/backup/success_test/data/* /data1/data/
        fi

		echo "正在执行systemctl stop universe-delivery.service"
		systemctl stop universe-delivery.service
		sleep 3
		if [ -d "/opsdeploy.db" ]; then
                echo "正在清理成功端目录"
				rm -rf /home/devops1/sk/delivery-tool/plt-universe-install-srv
				rm -rf /home/devops1/sk/delivery-tool/plt-universe-install-web
                rm -rf /opsdeploy.db
        fi

		if [ -d "/data1/platform_v5.bak" ]; then
                echo "正在清理platform backup数据"
                rm -rf /data1/platform_v5.bak
        fi
 
        if [ -d "/data1/data.bak.v5" ]; then
                echo "正在清理data backup数据"
                rm -rf /data1/data.bak.v5
        fi

		echo "正在启动docked"
		systemctl start docker

		sleep 10

		echo "正在启动database"
		cd /home/devops1/sk/product/database
		bash start_database.sh
		sleep 1

		echo "正在启动platform"
		cd /home/devops1/sk/product/platform
		bash start_platform.sh
		sleep 1

		echo "正在启动dcm-rendering"
		cd /home/devops1/sk/product/dcm-rendering
		bash start_dcm-rendering.sh
		sleep 1
		
		echo "正在启动database"
		cd /home/devops1/sk/product/remote-rendering
		bash start_remote-rendering.sh
		sleep 1

		echo "正在启动cerebral"
		cd /home/devops1/sk/product/cerebral
		bash start_cerebral.sh
		sleep 1

		echo "正在启动ctpdoc"
		cd /home/devops1/sk/product/ctpdoc
		bash start_ctpdoc.sh
		sleep 1

		echo "正在启动thoracic"
		cd /home/devops1/sk/product/thoracic
		bash start_thoracic.sh
		sleep 1

		echo "正在启动jupiter"
		cd /home/devops1/sk/product/jupiter
		bash start_jupiter.sh
		sleep 1

		docker pull harbor.democompany.net:5050/shstorage/plt-alg-funcs:0.99.0
		docker pull harbor.democompany.net:5050/alg/coronary/cta:v5.7.1.rc1-cuda-11
		docker pull harbor.democompany.net:5050/alg/stroke/alg_cerebral_ctp:5.7.1.2.cuda11
		docker pull harbor.democompany.net:5050/alg/jupiter/engineering/release:2.7.1_hotfix8


fi





