import json

data = {
  'EventName': 's3:ObjectCreated:Put',
  'Key': 'album/F-IWpYvbAAEDiwY.jpg',
  'Records': [{
    'eventVersion': '2.0',
    'eventSource': 'minio:s3',
    'awsRegion': '',
    'eventTime': '2024-03-13T05:10:49.089Z',
    'eventName': 's3:ObjectCreated:Put',
    'userIdentity': {'principalId': 'lizhuo'},
    'requestParameters': {'principalId': 'lizhuo', 'region': '', 'sourceIPAddress': '120.208.45.150'},
    'responseElements': {
        'x-amz-id-2': 'dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8',
        'x-amz-request-id': '17BC3AD5F10E0A2C',
        'x-minio-deployment-id': '77e0a2bf-04d1-424e-83e7-957d91e46d67',
        'x-minio-origin-endpoint': 'http://172.31.0.2:9000'},
    's3': {
        's3SchemaVersion': '1.0',
        'configurationId': 'Config',
        'bucket': {'name': 'album', 'ownerIdentity': {'principalId': 'lizhuo'}, 'arn': 'arn:aws:s3:::album'},
        'object': {
          'key': 'F-IWpYvbAAEDiwY.jpg',
          'size': 10953,
          'eTag': '53bf8b24a4bca6f0bd42852332887afe', 'contentType': 'image/jpeg',
          'userMetadata': {'content-type': 'image/jpeg'},
          'sequencer': '17BC3AD5F393A75D'}},
    'source': {
        'host': '120.208.45.150',
        'port': '',
        'userAgent': 'MinIO (linux; amd64) minio-go/v7.0.68 MinIO Console/(dev)'}}
  ]
}

# 转换为json格式的字符串
data = json.dumps(data)
print(data)