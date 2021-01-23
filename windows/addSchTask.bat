echo off

set cpath=%~dp0check.py
echo -----------------------------
echo 当前路径：%cpath%
echo -----------------------------
schtasks /Create /SC DAILY /TN healthCheck9 /TR %cpath% /ST 09:30
schtasks /Create /SC DAILY /TN healthCheck16 /TR %cpath% /ST 16:10
echo -----------------------------
echo 添加9：30和16：10的计划任务成功
echo -----------------------------
pause
