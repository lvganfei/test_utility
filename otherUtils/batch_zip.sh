#!/usr/bin/env bash
source_dir=$1
target=$2
set -xv
#每100个目录打包成一个压缩文件
IFS=$'\n'
count=0
while [ `ls $source_dir|wc -l` -gt 0  ]
do
    mkdir $target/tmp
    cd $source_dir
    ls |head -n 100| xargs -n1 -I {} mv {} $target/tmp
    cd $target
    tar -zcvf batch_zip_$count.tar.gz tmp
    ((count=$count+1))
    rm -rf $target/tmp
done
