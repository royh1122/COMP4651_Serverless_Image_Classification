# Comparative Analysis of Serverless and Server-Based Architectures for Image Classification Deployment

This repository contains the implementation of our project comparing **serverless** and **server-based** architectures for deploying an image classification model. It demonstrates how to set up and test these architectures using **OpenFaaS** (serverless) and a **Flask-based server** (server-based) for a **MobileNetV2** model.

For more details on the project objectives, methodology, results, and analysis, please refer to the **[Project Report](./COMP4651_Group_8_Project_Report.pdf)**.

---

## ⚙️ Environment Setup

### 1. Serverless Deployment with OpenFaaS

#### Prerequisites
- **Docker**: Ensure Docker is installed and running.
- **Minikube**: A Kubernetes distribution for local development.
- **kubectl**: Kubernetes command-line tool for interacting with the cluster.
- **OpenFaaS CLI (`faas-cli`)**: OpenFaaS command-line tool for managing functions.
- For detailed installation instructions, refer to the **[OpenFaaS Workshop](https://github.com/openfaas/workshop)**.

#### Steps
1. **Run the setup script**:
   Navigate to the `serverless/` directory and execute the `setup-openfaas.sh` script:
   ```bash
   ./setup-openfaas.sh
   ```
   This script automates the following steps:
   1. Starts Minikube.
   2. Installs OpenFaaS using `arkade`.
   3. Sets up port forwarding for the OpenFaaS Gateway.
   4. Logs into OpenFaaS.
   5. Prepares the Python 3 Flask template for function creation.

2. **Individual Steps (if the script fails)**:
   1. Start Minikube:
        ```bash
        minikube start
        ```
   2. Install OpenFaaS using `arkade`:
        ```bash
        arkade install openfaas
        ```
   3. Set up port forwarding for the OpenFaaS Gateway:
        ```bash
        kubectl port-forward svc/gateway -n openfaas 8080:8080 &
        export OPENFAAS_URL="http://127.0.0.1:8080"
        ```
   4. Log into OpenFaaS:
        ```bash
        PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
        echo -n $PASSWORD | faas-cli login --username admin --password-stdin -g $OPENFAAS_URL
        ```
   5. Pull the Python 3 Flask template:
        ```bash
        faas-cli template store pull python3-flask
        ```

3. **Build and Deploy the Function**:
   1. Log in to Docker:
        ```bash
        docker login
        ```
   2. Build, push, and deploy the function using the provided YAML file:
        ```bash
        faas-cli up -f image-classify.yml
        ```


### 2. Server-Based Deployment with Flask

#### Prerequisites
- Python 3.8+ installed.
- Required Python packages (`Flask`, `TensorFlow`, etc.) listed in `server/requirements.txt`.

#### Steps
1. **Install Dependencies**:
   Navigate to the `server/` directory and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the Server**:
   Start the Flask API by executing:
   ```bash
   python server_api.py
   ```


### 3. Exposing the Server with Ngrok

To make your server accessible from external networks:

1. **Download Ngrok**:
   Visit the [Ngrok official website](https://ngrok.com) and download the appropriate version for your system.

2. **Sign Up and Authenticate**:
   - Sign up for a free Ngrok account to get an authentication token.
   - Authenticate Ngrok with your token:
     ```bash
     ngrok authtoken <your-authentication-token>
     ```

3. **Run a Tunnel**:  
   - Start a tunnel to expose the local server running on your desired port (replace `<port>` with the port number your server is running on, e.g., `8080`):
     ```bash
     ngrok http <port>
     ```
   - Ngrok will provide a public URL that you can use to access your server.

For more details, visit the **[Ngrok Getting Started Guide](https://ngrok.com/docs/getting-started/)**.

---

## 📊 Performance Testing

This section guides you through testing the performance of the serverless and server-based deployments. The provided Jupyter notebook benchmarks key metrics such as latency and throughput to compare the two architectures under varying load conditions.

#### Prerequisites
- **Serverless and Server-Based Deployments**: Ensure both deployments are running and accessible. Preferably, expose them through Ngrok to allow external access.
- **Ngrok**: Use the public URLs provided by Ngrok for the performance testing.
- **Jupyter Notebook**: Ensure you have Jupyter Notebook installed to open and run the `performance_test.ipynb` file.

#### Steps
1. Navigate to the `tests/` directory.
2. Open and run the `performance_test.ipynb` notebook.
3. Follow the Notebook Instructions, run the cells sequentially to benchmark the performance of the serverless and server-based deployments. The notebook will measure metrics such as:
    - **Latency**: The time taken to process a single inference request.
    - **Throughput**: The number of requests handled per second.

---

## 📑 Report

For a detailed discussion of the methodology, results, and observations, please read the **[Project Report](./COMP4651_Group_8_Project_Report.pdf)**.

---

## 👨‍💻 Authors

- **HUANG, I-wei** (SID: 20824074, ITSC: ihuangaa)
- **LI, Yu-hsi** (SID: 20819823, ITSC: ylils)
- **LIN, Yen-po** (SID: 20819782, ITSC: ylindr)