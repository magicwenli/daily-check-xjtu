#!/bin/bash
# set -x


echo “添加cron.txt到crontab”
crontab /opt/dailycheck/cron.txt

echo “运行 daily-check.py”
python3 /opt/dailycheck/daily-check.py
