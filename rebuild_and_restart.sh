#!/bin/bash

# 停止并删除指定的容器
docker rm -f qywxmessage_rabbitmq1
docker rm -f qywxmessage_rabbitmq2

# 删除指定的镜像
docker rmi qywxmessage_rabbitmq:latest 

# 重新构建 Docker 镜像
docker build -t qywxmessage_rabbitmq:latest .

# 运行新的 Docker 容器 
docker run -it -d --name=qywxmessage_rabbitmq1 qywxmessage_rabbitmq:latest
docker run -it -d --name=qywxmessage_rabbitmq2 qywxmessage_rabbitmq:latest
