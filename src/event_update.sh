#!/usr/bin/env bash

echo $(date)

source ../venv/bin/activate
if python --version == '2.7.4';then
    echo 'dynamic_update_event.py start'
    python dynamic_update_event.py
fi
echo 'Update Finished'

sleep 5s

echo 'Save Event to MySQL'
python event2mysql.py