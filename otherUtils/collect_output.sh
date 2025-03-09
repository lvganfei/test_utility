#!/usr/bin/env bash
case_list=$1

for case_num in `cat $case_list`
  do
    echo $case_num | awk '{echo $1 $2}'| 
  done