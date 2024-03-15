import hashlib
import base64
import os
import requests

class WeComBot:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_message(self, message):
        try:
            payload = {
                "msgtype": "text",
                "text": {
                    "content": message
                }
            }
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            if response.status_code == 200:
                print('Message sent successfully to WeCom bot')
            else:
                print(f'Message sending failed: {response.content.decode()}')
        except Exception as e:
            print(f'Message sending failed: {e}')

    def send_image(self, image_path):
        try:
            img_data = self._image_to_img_data(image_path)
            print("Image data successfully loaded.")
            md5_hash = hashlib.md5(img_data).hexdigest()
            img_base64 = base64.b64encode(img_data).decode('utf-8')
            print(image_path,"图片i地址")
            payload = {
                "msgtype": "image",
                "image": {
                    "base64": img_base64,
                    "md5": md5_hash
                }
            }
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            if response.status_code == 200:
                print('Image sent successfully to WeCom bot')
            else:
                print(f'Image sending failed: {response.content.decode()}')
        except FileNotFoundError:
            print(f'Image file not found: {image_path}')
        except Exception as e:
            print(f'Image sending failed: {e}')

    def _image_to_img_data(self, image_path):
        if image_path.startswith('http'):
            response = requests.get(image_path)
            if response.status_code != 200:
                raise ValueError(f"Failed to fetch image from URL: {image_path}")
            img_data = response.content
        else:
            if not self._is_valid_image(image_path):
                raise ValueError(f"Invalid image file: {image_path}")
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
        return img_data

    def _is_valid_image(self, image_path):
        if not os.path.exists(image_path):
            return False
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        if not any(image_path.lower().endswith(ext) for ext in allowed_extensions):
            return False
        return True
# webhook_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4e35a96d-134b-45fa-9c5a-f3d4f65670f6'
# bot = WeComBot(webhook_url)
#
# bot.send_image("./ico.png")
# bot.send_image("http://1.15.7.2:9000/picshow/ip_kaoyan/202403120130025.png")
