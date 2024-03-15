from datetime import datetime
from host_ip import get_myhost_ip
import pika
import json
from qywxtools import WeComBot
from redismoudle import AccessLimit
from  mysqle import DatabaseManager

class RabbitMQClient:
    def __init__(self, username, password, host, port, virtual_host, exchange, exchange_type, queue):
        self._credentials = pika.PlainCredentials(username=username, password=password)
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, virtual_host=virtual_host, credentials=self._credentials)
        )
        self._channel = self._connection.channel()
        self._exchange = exchange
        self._exchange_type = exchange_type
        self._queue = queue
        self._channel.exchange_declare(exchange=self._exchange, exchange_type=self._exchange_type)
        self._channel.queue_declare(queue=self._queue, durable=True)
        self._channel.queue_bind(exchange=self._exchange, queue=self._queue)
        self.access_limit = AccessLimit()

        print(f'Queue "{self._queue}" is bound to exchange "{self._exchange}". Waiting for messages. To exit press CTRL+C')

    def callback(self, ch, method, properties, body):
        try:
            self.handlebody(body)
        except Exception as e:
            print("消息发送出错了",e)

    # 处理逻辑
    def handlebody(self,body):
        # 判断是否为上一条ip 是的话跳过
        # 判断是否为上一张图片，是的话跳过
        data = json.loads(body)
        # print("Received message: ", data)
        # print(data['EventName'])
        HOST_URL = "http://1.15.7.2:9000/"
        event_time = data['Records'][0].get('eventTime', '')
        source_ip_address = data['Records'][0].get('requestParameters', {}).get('sourceIPAddress', '')
        user_agent = data['Records'][0].get('source', {}).get('userAgent', '')
        size = data['Records'][0].get('s3', {}).get('object', {}).get('size', '')
        name = data['Records'][0].get('s3', {}).get('bucket', {}).get('name', '')
        bucket_name = data['Records'][0]['s3']['bucket']['name']
        event_name = data['Records'][0]['eventName']
        content_type = data['Records'][0].get('s3', {}).get('object', {}).get('contentType', '')
        local_ip_address = get_myhost_ip()
        upload_time = datetime.now()
        object_name = data['Key']
        image_url = HOST_URL + object_name  # 更改为你的图片地址

        log_message = f"事件时间：{event_time}, 源IP地址：{source_ip_address}, 用户代理：{user_agent}, 尺寸：{size}, 名称：{object_name}, 桶名：{bucket_name}, 事件名：{event_name}, 内容类型：{content_type}, 本地IP地址：{local_ip_address}, 上传时间：{upload_time}"


        # 同一个图片不用多次存储
        key_bool = self.access_limit.get_value(object_name, 1, 5)
        if key_bool:
            try:
                self.access_limit = AccessLimit()
                event_name_bool = self.access_limit.get_value(event_name, 1, 1)
                source_ip_address_bool = self.access_limit.get_value(source_ip_address, 5, 30)
                # print("event_name_bool,source_ip_address_bool,key_bool",event_name_bool,source_ip_address_bool,key_bool)
                bool = (event_name_bool and source_ip_address_bool and key_bool)
                # bool = (event_name_bool and source_ip_address_bool)
                # print("有一个假全是假：",bool)
                if bool:
                    # print("是True","下面有消息",",是False,下面没有消息")
                    self.send_all(log_message, image_url, content_type, bucket_name)



            except Exception as e:
                print(e)
                self.send_message(f'redis 出现问题了,{e}')

            # 使用示例
            # mysql处理

            self.mysqlhadle(data, HOST_URL, local_ip_address)


    def mysqlhadle(self,data,HOST_URL,local_ip_address):
        try:
            db = DatabaseManager("1.15.7.2", 3306, "pyqywx", "Ka2fphma26zfyWHZ", "pyqywx")
            db.check_create_table("records")

            # data = ... # TODO: 输入你的数据
            # host_url = ... # TODO: 输入你的图片地址
            # get_host_ip = ... # TODO: 输入获取IP地址的函数

            db.insert_into_table("records", data=data, host_url=HOST_URL, get_host_ip=local_ip_address)

        except Exception as e:
            self.send_message("myql存储消息出错了,", e)


    def send_all(self, log_message, image_url, content_type, bucket_name):
        self.send_message(log_message)
        if "image" in content_type.lower() :
            if bucket_name != "zeaburmemos":
                if self.access_limit.get_value(content_type, 1, 10):
                    # print("10秒钟一次图片")
                    self.send_img(image_url)
        
    def send_message(self,message):
        webhook_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4e35a96d-134b-45fa-9c5a-f3d4f65670f6'
        bot = WeComBot(webhook_url)

        bot.send_message(message)
    def send_img(self,imgurl):
        webhook_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4e35a96d-134b-45fa-9c5a-f3d4f65670f6'
        bot = WeComBot(webhook_url)

        bot.send_image(imgurl)
    def start_consume(self):
        self._channel.basic_consume(queue=self._queue, on_message_callback=self.callback, auto_ack=True)
        self._channel.start_consuming()

# 使用该类
client = RabbitMQClient(username='gwozai', password='123456', host='1.15.7.2', port=5672, virtual_host='/', exchange='bucketevents', exchange_type='fanout', queue='miniomessage')
client.start_consume()