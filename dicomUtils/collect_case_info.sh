#! /bin/bash
# echo $1
root=$1
# get folder list which contains dicoms
folderList=''
function getdir(){
    echo 'root is '$1
    rootList=`find $1 -maxdepth 1 -type d | sed -n '2,$p'`

    for element in $rootList
      do
        # elementList=`find $element -maxdepth 1 -type d | sed -n '2,$p'`
        elementcount=`find $element -maxdepth 1 -type d | sed -n '2,$p' | wc -l`
        # echo 'element count: '$elementcount
        if [[ $elementcount -eq 0 ]] && [[ "`ls -A $element | wc -l`" > 1 ]]
        then
            folderList="$folderList,$element"
        else
            # echo $element" is folder"
            getdir $element
        fi
        unset element
     done

    
}

getdir "$root"

echo $folderList

echo "folder_name,study_instance_uid,series_instance_uid,patient_id,patient_name,study_date,series_date,study_description,series_description,hospital,manufacturer,patientage,patientsex" >> "$root"/all_case_info.csv
for case in `echo $folderList | xargs -d ',' -n1 echo -e`;
    do  
        if [ -d $case ]
        then
            dcmcount=`find $case  -type f | wc -l`
            echo $dcmcount
            if [ "$dcmcount" = 0 ]
            then
               echo 'empty case'
               rm -fr $case
               continue
            fi
            firstdcm=`find $case  -type f | head -n 1`
            echo $firstdcm
            # check if the first dcm is valid
            isdcm=`dcmftest $firstdcm | awk -F ':' '{print $1}'`
            if [[ "$isdcm" = 'yes' ]]
            then
                study_instance_uid=`dcmdump -L --search 0020,000d $firstdcm  |  awk -F '[' '{print $2}'| awk -F ']' '{print $1}'`
                echo $study_instance_uid
                series_instance_uid=`dcmdump -L --search 0020,000e $firstdcm |  awk -F '[' '{print $2}'| awk -F ']' '{print $1}'`
                echo $series_instance_uid
                patient_id=`dcmdump -L --search 0010,0020 $firstdcm |  awk -F '[' '{print $2}'| awk -F ']' '{print $1}'`
                echo $patient_id
                patient_name=`dcmdump -L --search 0010,0010 $firstdcm |  awk -F '[' '{print $2}'| awk -F ']' '{print $1}'`
                echo $patient_name
                study_date=`dcmdump -L --search 0008,0020 $firstdcm |  awk -F '[' '{print $2}'| awk -F ']' '{print $1}'`
                echo $study_date
                series_date=`dcmdump -L --search 0008,0021 $firstdcm |  awk -F '[' '{print $2}'| awk -F ']' '{print $1}'`
                echo $series_date
                study_description=`dcmdump -L --search 0008,1030 $firstdcm |  awk -F '[' '{print $2}'| awk -F ']' '{print $1}'`
                echo $study_description
                series_description=`dcmdump -L --search 0008,103e $firstdcm |  awk -F '[' '{print $2}'| awk -F ']' '{print $1}'`
                echo $series_description
                
                hospital=`dcmdump -L --search 0008,0080 $firstdcm |  awk -F '[' '{print $2}'| awk -F ']' '{print $1}'`
                echo $hospital
                
                manufacturer=`dcmdump -L --search 0008,0070 $firstdcm |  awk -F '[' '{print $2}'| awk -F ']' '{print $1}'`
                echo $manufacturer

                patientage=`dcmdump -L --search 0010,1010 $firstdcm |  awk -F '[' '{print $2}'| awk -F ']' '{print $1}'`
                patientsex=`dcmdump -L --search 0010,0040 $firstdcm |  awk -F '[' '{print $2}'| awk -F ']' '{print $1}'`
                
                sleep 1s

                line="$case,$study_instance_uid,$series_instance_uid,$patient_id,$patient_name,$study_date,$series_date,$study_description,$series_description,$hospital,$manufacturer,$patientage,$patientsex"
                echo $line >> "$root"/all_case_info.csv
                
                echo "$case finished, write csv"
                unset case
                unset study_instance_uid
                unset series_instance_uid
                unset patient_id
                unset patient_name
                unset study_date
                unset series_date
                unset study_description
                unset series_description
                unset hospital
                unset manufacturer
                unset patientage
                unset patientsex
                unset line
            else
                echo $firstdcm' is not dcm format'
            fi

        else
            # echo $dir_or_file
            echo  "$dir_or_file is a file"
        fi
    done

echo 'all finished'
echo 'all_case_info.csv file dumped'
