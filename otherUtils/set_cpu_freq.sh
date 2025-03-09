#!/usr/bin/env bash

#sudo apt-get install cpufrequtils -y
cpunum=$(cpufreq-info |grep analyzing|wc -l|awk '{print int($0)}')
for i in $(seq 0 $[$cpunum-1])
do
   sudo cpufreq-set -c $i -g performance
   cat /sys/devices/system/cpu/cpu$i/cpufreq/scaling_governor
   echo "cpu" $i "be set performance"
done