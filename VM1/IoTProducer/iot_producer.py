import json
import time
import random
import base64
import cv2
from kafka import KafkaProducer
from tensorflow.keras.datasets import cifar10


# Path to Kafka messages
KAFKA_MESSAGES_PATH = "../../data/kafka_messages/kafka_messages.json"

# Load data
with open(KAFKA_MESSAGES_PATH, 'r') as f:
    messages = json.load(f)

# Simulate sending messages
for message in messages:
    print(f"Produced message: {message}")
# Load CIFAR-10 dataset
(trainX, trainY), (_, _) = cifar10.load_data()
imageTypes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

# Assign a unique ProducerID
PRODUCER_ID = "producer1"  # Change this for different producers (e.g., producer2)

def get_random_image():
    """Select a random image and its label."""
    i = random.randint(0, len(trainX) - 1)
    image = trainX[i]
    label = imageTypes[trainY[i][0]]
    return image, label

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers="192.168.5.22:9092",  # Replace with your Kafka broker's IP (VM3)
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for i in range(100):  # Example: send 100 images
    image, label = get_random_image()
    _, buffer = cv2.imencode('.jpg', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    data = {
        "ID": i,
        "GroundTruth": label,
        "Data": image_base64,
        "ProducerID": PRODUCER_ID  # Include ProducerID in the message
    }

    producer.send('iot_images', value=data)
    producer.flush()
    print(f"Sent image {i} with label {label} from {PRODUCER_ID}")
    time.sleep(1)

producer.close()