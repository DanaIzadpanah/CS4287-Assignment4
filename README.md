CS4287-Assignment4: IoT Data Analytics with Apache Spark Batch Processing

Overview

This project builds upon Assignment 3 by adding batch processing capabilities using Apache Spark. The primary goal is to analyze IoT inference data stored in MongoDB and calculate the number of errors made by the inference server for each producer using the MapReduce approach. The project integrates Spark-based batch processing into the existing Kubernetes-deployed pipeline, enabling efficient analysis of large-scale data.

Technologies Used
	•	Apache Kafka: Streams and manages the message queue between IoT producers and consumers.
	•	Apache Spark: Performs batch processing and MapReduce error analysis.
	•	MongoDB: Stores processed image data and metadata for analysis.
	•	Python: Main programming language, using libraries like PySpark, kafka-python, pymongo, and Flask.
	•	Flask: Hosts the machine learning inference model (ResNet50).
	•	TensorFlow: Used for loading the pre-trained ResNet50 ML model.
	•	Docker: Containerized deployment for Kafka, MongoDB, and the ML server.
	•	Kubernetes: Manages container orchestration for scalability and reliability.
	•	Chameleon Cloud: Cloud platform for provisioning virtual machines.

Project Architecture

The pipeline includes four virtual machines (VMs), with Apache Spark integrated for batch processing:
	•	VM1: IoT Producer
	•	VM2: ML Model (ResNet50) Inference Server
	•	VM3: Kafka Broker & Consumers
	•	VM4: MongoDB and Apache Spark

VM1: IoT Producer
	•	Role: Generates synthetic image data with GroundTruth labels and sends it to Kafka.
	•	Details:
	•	The producer uses kafka-python to send messages to Kafka, including metadata like GroundTruth, ProducerID, and the image data encoded in base64.

VM2: ML Inference Server
	•	Role: Processes images in real time using the ResNet50 model hosted on Flask.
	•	Details:
	•	Accepts base64-encoded image data from the Kafka consumer and returns the Inferred label.

VM3: Kafka Broker & Consumers
	•	Role: Handles message distribution between the producer and consumers.
	•	Details:
	•	Kafka Broker: Routes messages to consumers.
	•	DB Consumer: Stores image metadata and inference results in MongoDB.
	•	Inference Consumer: Sends images to the Flask server for inference and updates MongoDB with the results.

VM4: MongoDB and Apache Spark
	•	Role: Stores data for batch processing and executes Spark MapReduce jobs.
	•	Details:
	•	MongoDB stores GroundTruth, Inferred labels, and ProducerID for each message.
	•	Apache Spark performs batch processing to calculate errors per producer.

Installation & Setup

Prerequisites
	•	Set up 4 VMs (VM1-VM4) on Chameleon Cloud with Ubuntu 22.04.
	•	Install Docker, Kubernetes, Python 3, and Apache Spark on the respective VMs.
	•	Configure Kubernetes with kubectl access from the control node.

Step-by-Step Setup

Ansible Playbooks
	1.	Run the Ansible playbooks to provision the VMs and install necessary components:
ansible-playbook playbook_master_test.yaml

Kubernetes Deployment
	1.	Deploy all components using the provided Kubernetes YAML files:
 kubectl apply -f kubernetes_yamls/kafka_deployment.yaml
kubectl apply -f kubernetes_yamls/mongo_deployment.yaml
kubectl apply -f kubernetes_yamls/ml_inference_deployment.yaml
kubectl apply -f kubernetes_yamls/producer_job.yaml
kubectl apply -f kubernetes_yamls/consumer_job.yaml


Confirm Component Status
	1.	Verify that all pods are running in Kubernetes:
 kubectl get pods

 
How the System Works
	1.	The IoT Producer (VM1) generates synthetic image data with GroundTruth labels and sends it to the Kafka broker (VM3).
	2.	The Kafka Broker (VM3) routes messages to the DB Consumer and Inference Consumer.
	3.	The DB Consumer (VM3) stores image metadata in MongoDB (VM4).
	4.	The Inference Consumer (VM3) sends image data to the Flask server (VM2), retrieves the Inferred label, and updates MongoDB with the result.
	5.	The Spark Job (VM4) reads data from MongoDB, performs batch processing to calculate inference errors, and outputs the results in a CSV file.

Spark Batch Processing

MapReduce Job

The Apache Spark job calculates errors by comparing the GroundTruth and Inferred labels for each producer:
	1.	Reads data from MongoDB.
	2.	Calculates whether each inference is correct or incorrect.
	3.	Aggregates errors per producer using the MapReduce approach.
	4.	Outputs the error counts as a CSV file.

Running the Spark Job
	1.	Navigate to the Spark job directory:
 cd spark_job/
 	2.	Execute the Spark job:
  spark-submit spark_mapreduce_error_count.py

  
Output

The results will be saved in a CSV file:
	•	Location: data/spark_output/error_counts_per_producer.csv
	•	Sample Output:
 ProducerID,total_errors
producer1,2
producer2,1

Project Structure

Assignment4/
├── ansible_playbooks/        # Ansible playbooks for setup
├── kubernetes_yamls/         # Kubernetes YAML files for deployment
├── data/                     # Data for Spark input/output
│   ├── mongo_data/           # MongoDB data
│   ├── spark_output/         # Spark output CSV files
├── VM1/                      # IoT Producer code and Dockerfile
├── VM2/                      # ML Inference Server code and Dockerfile
├── VM3/                      # Kafka Consumers and Dockerfile
├── VM4/                      # MongoDB and Spark setup
├── spark_job/                # Spark MapReduce job scripts
└── README.md                 # This README file

Team Contributions
	•	Micah Bronfman: Implemented Spark integration with MongoDB and developed the Spark MapReduce job for error analysis. Managed integration with the Kubernetes-deployed pipeline.
	•	Jonathan Tilahun: Enhanced Kafka consumer scripts to track inference accuracy and set up Spark configurations for batch processing.
	•	Dana Izadpanah: Assisted with Kubernetes deployments, particularly for scaling MongoDB and Spark. Conducted testing and validation of the Spark output.

Conclusion

This project demonstrates the integration of Apache Spark into the existing IoT pipeline for efficient batch processing and error analysis. The Spark MapReduce job ensures scalable and accurate computation of inference errors across large datasets, enhancing the pipeline’s analytical capabilities.
