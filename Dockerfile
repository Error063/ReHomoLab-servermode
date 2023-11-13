FROM python:3.11-slim-buster
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 9000
CMD ["python3.11", "app.py"]

