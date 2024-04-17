# pymessagerabbitmq

PyMessengerabbitmq是一个使用了RabbitMQ、Redis和Minio的工具。其主要功能是配置Minio的RabbitMQ，然后通过RabbitMQ将消息传递给企业微信机器人。

## 代办
* Redis的代码设计灵活，待进一步优化。
* 配置文件需进一步分离以便于管理。
* 支持通过Docker进行环境变量的传递。
* 可进行服务器IP、账号密码的自动配置，并能够完成自动部署。

## 使用Docker
PyMessengerabbitmq的Docker镜像实现了环境变量的传递，同时还支持自动部署到服务器上。

### TODO
1. 完善服务器操作，实现镜像的拉取更新。

#### 服务器操作
* 拉取镜像，更新

#### 一种方式
运行以下命令进行部署：

```
docker-compose up -d
```

#### 另一种方式
运行以下命令进行部署：

```
docker stop pymessagerabbitmq & docker rm pymessagerabbitmq & docker rmi gwozai/pymessagerabbitmq & docker pull gwozai/pymessagerabbitmq & docker run -it -d --name pymessagerabbitmq gwozai/pymessagerabbitmq
```

未来将会进一步实现若依框架的镜像自动打包，并部署到服务器。




使用的工具：
- rabbitmq
- redis
- minio
配置minio的rabbitmq，然后使用rabbitmq把消息传递给企业微信机器人。
- [ ] redis代码需要改进
- [ ] 配置文件需要抽出
- [ ] 用docker传递变量
- [ ] 配置服务器的ip，账号密码，可以自动部署

docker镜像传递参数，传递环境变量。   
要自动部署到服务器上，


### TODO
若依框架的镜像自动构建打包代码并做成docker镜像 

#### 服务器操作
拉取镜像，更新



方式一:   
docker-compose up -d

方式二:   
docker stop pymessagerabbitmq & docker rm pymessagerabbitmq & docker rmi gwozai/pymessagerabbitmq & docker pull gwozai/pymessagerabbitmq & docker run -it -d --name pymessagerabbitmq gwozai/pymessagerabbitmq




若依框架的镜像自动打包，并部署到服务器
