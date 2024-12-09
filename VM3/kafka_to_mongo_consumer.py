from kafka import KafkaConsumer
from pymongo import MongoClient
import json
import requests

# MongoDB connection
mongo_client = MongoClient("mongodb://192.168.5.206:27017/")
mongo_db = mongo_client["kafkaDatabase"]
mongo_collection = mongo_db["iot_images_collection"]


# Path to MongoDB data
MONGO_ENTRIES_PATH = "../../data/mongo_data/mongo_entries.json"

# Load data
with open(MONGO_ENTRIES_PATH, 'r') as f:
    entries = json.load(f)

# Simulate MongoDB insertion
for entry in entries:
    print(f"Inserted into MongoDB: {entry}")

# Kafka consumer setup
consumer = KafkaConsumer(
    'iot_images',
    bootstrap_servers=['192.168.5.22:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Flask inference server
INFERENCE_SERVER_URL = "http://192.168.5.207:5000/"

for message in consumer:
    data = message.value

    # Perform inference
    response = requests.post(INFERENCE_SERVER_URL, json={"image": data["Data"]})
    if response.status_code == 200:
        data["Inferred"] = response.json().get("inferred")
    else:
        data["Inferred"] = "error"

    # Insert into MongoDB
    mongo_collection.insert_one(data)
    print(f"Inserted into MongoDB: {data}")