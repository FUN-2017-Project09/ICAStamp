#!/bin/bash

binary_path=`dirname $0`
while :
do
if sudo python ${binary_path}/Raspygame.py
#if sudo python Raspygame.py
  then
    break
  fi
done

exit 0
