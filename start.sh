#!/bin/bash

# 以后台进程运行 Django 服务器
python3 DjangoPart/manage.py runserver 0.0.0.0:9012 &

# 等待 Django 服务器启动
sleep 5

# 显示浏览器窗口
open -a "Google Chrome" "http://127.0.0.1:9012/04money_arrange/#bill_subpage"
