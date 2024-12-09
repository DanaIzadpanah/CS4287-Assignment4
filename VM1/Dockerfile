FROM python:3.9-slim

# Install dependencies
RUN pip install kafka-python tensorflow opencv-python-headless

# Copy the producer script
COPY iot_producer.py /app/iot_producer.py

# Set the working directory
WORKDIR /app

# Run the producer script
CMD ["python", "iot_producer.py"]