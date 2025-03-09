#!/bin/bash


read -p "是否备份并清理老平台数据Y/N:" ARG


while true ; do
	if [ $ARG == N ] || [ $ARG == Y ];then
		break;
	fi
	read -p "请输入的是否正确参数Y/N:" ARG
	#statements
done

if [[ $ARG == Y ]];then
	echo "数据备份开始:\n"
	echo "正在关闭docker 服务"
	systemctl stop docker 

	sleep 30


	echo "正在备份mongodb数据"

	if [ -d "/data1/mongodb" ]; then
		cp -r  /data1/mongodb /data1/backup/success_test/mongodb
	fi


	echo "正在备份product"文件

	if [ -d "/home/devops1/sk/product" ]; then
		cp -r  /home/devops1/sk/product /data1/backup/success_test/product
	fi


	echo "正在备份mysql数据"


	if [ -d "/data0/mysql" ]; then
		cp -r  /data0/mysql /data1/backup/success_test/mysql
	fi


	if [ -d "/data1/mysql" ]; then
		cp -r  /data1/mysql /data1/backup/success_test/mysql_1
	fi

	echo "正在备份data数据"

	if [ -d "/data1/data" ]; then
		cp -r   /data1/data /data1/backup/success_test/data
	fi





fi





echo "正在启动docked"

systemctl start docker 



