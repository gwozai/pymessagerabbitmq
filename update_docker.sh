#!/bin/bash
# 停止容器
docker stop pymessagerabbitmq
# 删除容器
docker rm pymessagerabbitmq

# 删除镜像
docker rmi gwozai/pymessagerabbitmq

# 获取最新的镜像
docker pull gwozai/pymessagerabbitmq

# 运行新容器
docker run -it -d --name pymessagerabbitmq gwozai/pymessagerabbitmq