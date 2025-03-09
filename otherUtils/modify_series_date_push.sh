# /data1/platform-test/data/source/coronary/
count=0
root=$1
aet=$2

for case in `ls  $root`
    do  
        if [ $count -gt 20 ];
        then
            break
        fi
        dir_or_file="$root/$case"
        echo $dir_or_file
        if [ -d $dir_or_file ];
        then
            echo "$root/$case is a dir"
            dcmcount=`ls $root/$case | wc -l`
            if [ "$dcmcount" = 0 ];
            then
               echo 'empty case'
               continue
            fi
            echo '开始修改dcm 日期'
            datesd=$(( $count / 2 ))
            today=$((20230320+$datesd))
            if [ $today -gt 20230331 ];
            then
                break
            fi
            nowtime=`date +'%H%M%S.000000'`
            for dcm in `find $root/$case -name '*.dcm' -type f`
                do
                    dcmodify  -nb -ma "(0008,0020)=$today" -ma "(0008,0021)=$today" -ma "(0008,0030)=$nowtime" -ma "(0008,0031)=$nowtime" $dcm
                done
            # firstdcm=`ls $root/$case | head -n 1`
            # echo $firstdcm
            # series_instance_uid=`dcmdump -L --search 0020,000e $root/$case/$firstdcm | awk -F '[' '{print $2}'| awk -F ']' '{print $1}'`
            # echo $series_instance_uid
            # starttime=`date +'%Y-%m-%d %H:%M:%S'`
        
            # echo -n "$series_instance_uid,$starttime," >> push_time_statistic_"$JOB_BASE_NAME"_"$SERVICE"_"$today".csv
            storescu -v  -aec SKDICOMINT -aet $aet 10.14.10.200 11112 +sp *.dcm +sd +r "$root/$case/"
            storescu -v  -aec SKDICOMINT -aet $aet 10.14.10.216 11112 +sp *.dcm +sd +r "$root/$case/"
            
            
            count=$(($count+1))
            # endtime=`date +'%Y-%m-%d %H:%M:%S'`
            # echo $endtime >> push_time_statistic_"$JOB_BASE_NAME"_"$SERVICE"_"$today".csv
            # echo 'finish scu and sleep 300s'
           
            # sleep 1
            echo 'deal with another case'
        else
            # echo $dir_or_file
            echo  "$dir_or_file is a file"
        fi
    done

echo 'all finished'