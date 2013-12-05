@echo off
start /b tshark -i 1 -a duration:10000 -w Z:\pcaps\capture.pcap
start /b copy_beginning_cookies.bat
start /b driver.exe E:\screenshotcsharp.exe E:\start_driver.bat 1
exit