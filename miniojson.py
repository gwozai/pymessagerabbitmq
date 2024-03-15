from datetime import datetime
from socket import socket


def insert_data(self, data):
    HOST_URL = "http://1.15.7.2/9000/"
    event_time = data['Records'][0].get('eventTime', '')
    source_ip_address = data['Records'][0].get('requestParameters', {}).get('sourceIPAddress', '')
    user_agent = data['Records'][0].get('source', {}).get('userAgent', '')
    size = data['Records'][0].get('s3', {}).get('object', {}).get('size', '')
    name = data['Records'][0].get('s3', {}).get('bucket', {}).get('name', '')
    bucket_name = data['Records'][0]['s3']['bucket']['name']
    event_name = data['Records'][0]['eventName']
    content_type = data['Records'][0].get('s3', {}).get('object', {}).get('contentType', '')
    local_ip_address = socket.gethostbyname(socket.gethostname())
    upload_time = datetime.now()
    key = data['Key']
    image_url = HOST_URL + key # 更改为你的图片地址


    # 创建一个字典来保存所有返回的字段
    return_fields = {
        'eventTime': event_time,
        'sourceIPAddress': source_ip_address,
        'userAgent': user_agent,
        'size': size,
        'name': name,
        'bucketName': bucket_name,
        'eventName': event_name,
        'contentType': content_type,
        'localIPAddress': local_ip_address,
        'uploadTime': upload_time,
        'image_url': image_url
    }

    return return_fields