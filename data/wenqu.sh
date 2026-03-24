#!/bin/bash

# 安装依赖
poetry -C /opt/WenQu install >/dev/null 2>&1

poetry -C /opt/WenQu run /opt/WenQu/main.py 


