#! /bin.bash
#中台目录中有些包含多个序列，这个脚本通过输入文件夹列表，遍历每个文件夹中等dcm文件并将他们拆分到独立的文件夹中, $1 为文件夹列表
folder_list=$1
base_dir='/data1/universe-longrun-data/thoracic'
for folder in  `cat $folder_list`
do
    if [[ -d "$base_dir/$folder" ]]; then
        for dcm in `find "$base_dir/$folder" -name '*.dcm' -type f`;
        do
            
            seriesid=`dcmdump -L  --search 0020,000e $dcm | head -n 1 | awk -F '[' '{print $2}'| awk -F ']' '{print $1}'`
            
            if [[ -d "$base_dir/$seriesid" ]]; then
                echo 'series already exists'
                mv $dcm $base_dir/$seriesid/
            else
                echo 'series not exists, mk new folder'
                mkdir "$base_dir/$seriesid"
                mv $dcm $base_dir/$seriesid/
            fi
        done
            
    else
        echo 'not exist folder'
    fi
done