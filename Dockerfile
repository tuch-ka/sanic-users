FROM python:3
EXPOSE 8001

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH /app/src
