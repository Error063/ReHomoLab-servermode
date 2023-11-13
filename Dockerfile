FROM python:3.11-slim-buster
RUN apt-get update && apt-get install -y gcc
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["python3.11", "app.py"]
