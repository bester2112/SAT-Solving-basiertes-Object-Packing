#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <process-name>"
    exit 1
fi

process_name=$1

while true; do
    ps -e | grep $process_name >> ps_output.txt
    sleep 5
done
