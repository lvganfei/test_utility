#! /bin.bash
# 每隔0.5s获取kubepod 进程数和主机进程数
while true
do
 echo -n 'kubepod pids: ' >> pid.log
 cat /sys/fs/cgroup/pids/kubepods.slice/pids.current >> pid.log
 echo -n 'ps -aux pids: ' >> pid.log
 echo `ps -aux | wc -l` >> pid.log
 sleep 0.5s
done