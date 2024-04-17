# 使用官方的 Python 镜像作为基础
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制项目的 requirements.txt 到工作目录
COPY requirements.txt .

# 使用 pip 安装依赖
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制本地的源代码文件至工作目录
COPY .. .

# 设置启动命令
CMD ["python", "main.py"]
