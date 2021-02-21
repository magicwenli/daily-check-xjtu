#!/bin/bash
# set -x
echo “添加cron.txt到crontab”
crontab /opt/daily-check-xjtu/cron.txt

echo “运行 daily-check.py”
python3 /opt/daily-check-xjtu/daily-check.py
