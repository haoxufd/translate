#!/bin/bash

while true; do
    # 执行 Python 脚本
    python translate.py
    # 检查退出代码
    exit_code=$?
    if [ $exit_code -ne 0 ]; then
        echo "translate.py crashed with exit code $exit_code. Restarting..."
        sleep 1
    else
        echo "translate.py exited normally."
        break
    fi
done