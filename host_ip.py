import socket

def get_myhost_ip():
   try:
       # 获取主机名
       host_name = socket.gethostname()
       # 通过主机名来获取 IP
       host_ip = socket.gethostbyname(host_name)
       return host_ip
   except:
       print("Unable to get Hostname and IP")
       return None



