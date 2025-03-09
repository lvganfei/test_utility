#! /bin/bash
# remove space in dir
# example: bash remove_space.sh /Volumes/ruijin/华山CTP

root=$1
echo $root
echo  "$root/*"

function remove_space {
    rename 's/ /_/g' $1/*
    for f in `ls $1`
        do
            dname="$1/$f"
            echo $dname
            if [ -d $dname ]
            then
                echo 'rename folder'
                remove_space $dname
                # rename 's/ /_/g' $dname
            else
                echo 'not folder, rename file'
                # rename 's/ /_/g' $1/$folder
            fi
        done
}


rename 's/ /_/g' $root/*
for folder in `ls $root`
do
  if [ -d "$1/$folder" ]
  then
     remove_space "$1/$folder"
  fi
done