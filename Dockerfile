FROM python:3.11-slim-buster
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y gcc
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -i http://mirrors.tencent.com/pypi/simple/ --trusted-host mirrors.tencent.com -r requirements.txt
COPY . /app
EXPOSE 9000
CMD ["python3.11", "app.py"]

