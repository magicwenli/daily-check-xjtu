#!/bin/bash
# set -x
echo “添加cron.txt到crontab”
crontab /dailycheck/cron.txt

echo “运行 daily-check.py”
python3 /dailycheck/daily-check.py
