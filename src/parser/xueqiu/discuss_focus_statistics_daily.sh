#!/usr/bin/env bash

echo $(date)

#source ../venv/bin/activate

U_V1=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $1}'`
U_V2=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $2}'`
U_V3=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $3}'`

if [[ ${U_V1}.${U_V2}.${U_V3} == '3.7.2' ]];then
    echo 'xueqiu_discuss_daily.py start'
    python ./discuss_parser/xueqiu_discuss_daily.py

    sleep 5s

    echo 'xueqiu_focus_statistics.py start'
    python ./focus_parser/xueqiu_focus_statistics.py
    echo 'Finished'
else
    echo 'Virtualenv Start Failed，Event Update failed'
fi
