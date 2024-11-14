FROM python:3.8-slim
WORKDIR /app
COPY consumer.py /app/
RUN pip install kafka-python pymongo
CMD ["python", "consumer.py"]
