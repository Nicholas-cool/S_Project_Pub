#!/bin/bash

# 以后台进程运行 Django 服务器
python DjangoPart/manage.py runserver 0.0.0.0:9012 &

# 等待 Django 服务器启动
sleep 2

# 显示浏览器窗口
open -a "Firefox" "http://127.0.0.1:9022/04money_arrange/#bill_subpage"
