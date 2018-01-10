#!/bin/bash
while :
do
  if sudo python Raspygame.py
  then
    break
  fi
done

exit 0