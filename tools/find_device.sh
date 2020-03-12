#!/bin/bash

read -n 1 -s -r -p "REMOVE the dongle and press any key to continue."$'\n'
sleep 1
BEFORE=$(ls /dev)
read -n 1 -s -r -p "INSERT the dongle and press any key to continue."$'\n'
sleep 1
AFTER=$(ls /dev)
RESULT=$(diff <(echo "$BEFORE") <(echo "$AFTER") | grep ">")
[ -z "$RESULT" ] && echo "No device found." || echo -e "Found:\n$RESULT"
