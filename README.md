# CS4287-Assignment3: IoT Data Analytics Pipeline with Kubernetes and Latency Analysis

## Overview
This project builds upon Assignments 1 and 2, where we previously implemented a cloud-based IoT data analytics pipeline using Infrastructure-as-Code (IaC) with Ansible and containerized components using Docker. In Assignment 3, we transition the pipeline to a Kubernetes-based deployment, enabling greater scalability and management. We also perform latency analysis to evaluate the system’s performance under varying workloads.

## Technologies Used
- **Ansible**: For automating the provisioning and setup of VMs and Kubernetes on Chameleon Cloud.
- **Apache Kafka**: For streaming and managing the message queue between the IoT producers and consumers.
- **MongoDB**: Used for storing processed image data along with metadata.
- **Python**: Main programming language, including libraries like `kafka-python`, `pymongo`, and `Flask` for different components.
- **Flask**: Hosting the machine learning inference model (ResNet50).
- **TensorFlow**: Used for loading the pre-trained ResNet50 ML model.
- **Docker**: Containerized deployment for components such as Kafka, MongoDB, and the ML server.
- **Kubernetes**: Orchestrates containers for scalability and resilience in a cloud environment.
- **Chameleon Cloud**: Cloud platform where we deployed four virtual machines to distribute the different components of the pipeline.

## Project Architecture
The project is divided across four VMs, each hosting a containerized component of the system, with Kubernetes managing deployment:

- **VM1**: IoT Producer
- **VM2**: ML Model (ResNet50) Inference Server
- **VM3**: Kafka Broker & Consumers
- **VM4**: MongoDB Database

### VM1: IoT Producer
- **Role**: Simulates IoT camera devices sending images to Kafka.
- **Details**:
  - The Producer generates synthetic image data and sends it to Kafka, along with a timestamp for latency measurement.
  - It uses the `kafka-python` library to connect to Kafka.

### VM2: ML Inference Server
- **Role**: Hosts the ResNet50 model using Flask to perform real-time image inference.
- **Details**:
  - Flask API exposes an endpoint to accept base64-encoded image data and returns a classification label.
  - The ML model uses TensorFlow’s ResNet50 pre-trained model.

### VM3: Kafka Broker & Consumers
- **Role**: Hosts the Kafka broker, which manages the data pipeline between the IoT producer and the consumers.
- **Details**:
  - Kafka Broker runs within a Kubernetes-managed container.
  - **Consumers**:
    - **DB Consumer**: Consumes image data and stores it in MongoDB (hosted on VM4).
    - **Inference Consumer**: Sends image data to the Flask API hosted on VM2 for inference and updates MongoDB with the predicted label.

### VM4: MongoDB Database
- **Role**: Stores all incoming data from Kafka, including image metadata and inference results.
- **Details**:
  - MongoDB runs within a Kubernetes-managed container.
  - The DB Consumer inserts image metadata, and the Inference Consumer updates MongoDB with inference results.

## Installation & Setup

### Prerequisites
- Ensure you have a Chameleon Cloud account and have created 4 VMs (VM1-VM4) using Ubuntu 22.04.
- Install Docker, Ansible, and Python 3 on each VM.
- Kubernetes must be configured on the VMs, with `kubectl` access from the control node.

### Step-by-Step Setup

#### Ansible Playbooks
1. Run the Ansible playbooks located in `ansible_playbooks/` to provision the VMs and install Kubernetes.
    ```bash
    ansible-playbook playbook_master_test.yaml
    ```

#### Kubernetes Deployment
1. Use the Kubernetes YAML files in `kubernetes_yamls/` to deploy each component:
    ```bash
    kubectl apply -f kubernetes_yamls/kafka_deployment.yaml
    kubectl apply -f kubernetes_yamls/mongo_deployment.yaml
    kubectl apply -f kubernetes_yamls/ml_inference_deployment.yaml
    kubectl apply -f kubernetes_yamls/producer_job.yaml
    kubectl apply -f kubernetes_yamls/consumer_job.yaml
    ```

#### Confirm Component Status
1. Verify that all components are running in Kubernetes:
    ```bash
    kubectl get pods
    ```

## How the System Works
1. **IoT Producer (VM1)** generates synthetic image data with timestamps and sends it to the Kafka broker (VM3).
2. **Kafka Broker (VM3)** distributes messages to two consumers: the DB Consumer and the Inference Consumer.
3. **DB Consumer (VM3)** inserts image metadata into MongoDB (VM4).
4. **Inference Consumer (VM3)** sends the image to the ML Inference Server (VM2) for classification, then updates MongoDB with the predicted label.
5. The system uses timestamped messages to measure end-to-end latency, allowing analysis of performance under different loads.

## Latency Analysis

### Generating Latency Data
- The `consumer.py` script records the latency of each message by comparing timestamps and outputs the data to `results/latency_data.csv`.

### Generating CDF Plot
- Run `generate_cdf_plot.py` (in `results/`) to produce a CDF plot of the latency data:
    ```bash
    python results/generate_cdf_plot.py
    ```
- The plot will be saved as `latency_cdf_plot.png` in the `results/` folder.

## Project Structure
Assignment3/  
├── ansible_playbooks/        # Ansible playbooks for VM provisioning and Kubernetes setup  
├── kubernetes_yamls/         # Kubernetes YAML files for component deployments  
├── results/                  # Folder for latency data and CDF plot  
│   ├── latency_data.csv  
│   ├── latency_cdf_plot.png  
│   └── generate_cdf_plot.py  
├── VM1/                      # IoT Producer Dockerfile and code  
├── VM2/                      # ML Inference Server Dockerfile and code  
├── VM3/                      # Kafka Broker and Consumers Dockerfile and code  
├── VM4/                      # MongoDB Dockerfile and code  
└── README.md                 # This README file  

## Team Contributions
- **Micah Bronfman**: Led the development of Ansible playbooks, automating the setup and provisioning of VMs, installing essential services (Kafka, Docker, MongoDB), and configuring Kubernetes.
- **Jonathan Tilahun**: Co-developed the Kubernetes deployments for Kafka, MongoDB, ML Inference Server, Producer, and Consumer. Worked on generating and analyzing latency data, including the CDF plot, to assess system performance.
- **Dana Izadpanah**: Co-developed the Kubernetes deployments alongside Jonathan for all pipeline components. Contributed to the data analysis pipeline, including latency data collection and visualization for performance evaluation.


## Conclusion
This project demonstrates the use of Kubernetes for orchestrating a cloud-based IoT data analytics pipeline. All components (Producer, Consumer, Kafka, ML Server, and MongoDB) are now deployed in Kubernetes, ensuring scalability and resilience. The end-to-end latency was analyzed, and a CDF plot generated to visualize system performance under varying loads.
