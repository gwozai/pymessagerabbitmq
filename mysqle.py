import mysql.connector
from datetime import datetime
from mysql.connector import pooling

class SingletonType(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseManager(metaclass=SingletonType):
    def __init__(self, host, port, user, password, database):
        self.dbconfig = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database
        }
        self.pool = self.create_pool()


    def create_pool(self):
        return mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=20, **self.dbconfig)
    def check_create_table(self, table_name):
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = cursor.fetchone()

        if result:
            print("Table exists.")
        else:
            print("Table does not exist. Creating now...")
            cursor.execute("CREATE TABLE records (event_time VARCHAR(255), source_ip_address VARCHAR(255), user_agent VARCHAR(255), size INT, name VARCHAR(255), bucket_name VARCHAR(255), event_name VARCHAR(255), content_type VARCHAR(255), local_ip_address VARCHAR(255), upload_time DATETIME, object_name VARCHAR(255), image_url VARCHAR(255))")
        conn.close()

    def insert_into_table(self, table_name, data, host_url, get_host_ip):
        conn = self.pool.get_connection()
        cursor = conn.cursor()

        event_time = data['Records'][0].get('eventTime', '')
        source_ip_address = data['Records'][0].get('requestParameters', {}).get('sourceIPAddress', '')
        user_agent = data['Records'][0].get('source', {}).get('userAgent', '')
        size = data['Records'][0].get('s3', {}).get('object', {}).get('size', '')
        name = data['Records'][0].get('s3', {}).get('bucket', {}).get('name', '')
        bucket_name = data['Records'][0]['s3']['bucket']['name']
        event_name = data['Records'][0]['eventName']
        content_type = data['Records'][0].get('s3', {}).get('object', {}).get('contentType', '')
        local_ip_address = get_host_ip
        upload_time = datetime.now()
        object_name = data['Key']
        image_url = host_url + object_name

        sql = f"INSERT INTO {table_name} (event_time, source_ip_address, user_agent, size, name, bucket_name, event_name, content_type, local_ip_address, upload_time, object_name, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (event_time, source_ip_address, user_agent, size, name, bucket_name, event_name, content_type, local_ip_address, upload_time, object_name, image_url)

        cursor.execute(sql, val)
        conn.commit()
        conn.close()

# 使用示例
# db = DatabaseManager("1.15.7.2", 3306, "pyqywx", "Ka2fphma26zfyWHZ", "pyqywx")
# db.check_create_table("records")
# import str_moudle
#
#
# import json
#
#
# data = json.loads(str_moudle.data)
# host_url = "adfsdf"
# get_host_ip ="dsaf"
#
#
# print(data)
# print(host_url)
# print(get_host_ip)
# db.insert_into_table("records",data, host_url, get_host_ip)