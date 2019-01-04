#!/usr/bin/env bash

echo $(date)

source ../venv/bin/activate

U_V1=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $1}'`
U_V2=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $2}'`
U_V3=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $3}'`

if [[ ${U_V1}.${U_V2}.${U_V3} == '2.7.14' ]];then
    echo 'dynamic_update_event.py start'
    python dynamic_update_event.py

    sleep 5s

    echo 'Save Event to MySQL'
    python event2mysql.py
    echo 'Event Update Finished'
else
    echo 'Virtualenv Start Sailed，Event Update failed'
fi
