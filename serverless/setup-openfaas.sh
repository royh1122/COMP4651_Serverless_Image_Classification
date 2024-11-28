#!/bin/bash

# Start Minikube
minikube start

# OpenFaaS setup
arkade install openfaas

echo 'waiting for openfaas pod to get ready'
until $(kubectl get all -n openfaas | grep pod/gateway | grep -q Running); do
    echo -n '.'
    sleep 10
done
echo 'done'

# Tunnel between local computer and Kubernetes cluster
echo "Setting up port forwarding for OpenFaaS Gateway..."
kubectl port-forward svc/gateway -n openfaas 8080:8080 &
jobs

# Set OpenFaaS URL environment variable
export OPENFAAS_URL="http://127.0.0.1:8080"

# Retrieve OpenFaaS admin password
PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
echo -n $PASSWORD | faas-cli login --username admin --password-stdin -g $OPENFAAS_URL

# List available functions
echo "Listing available functions in OpenFaaS:"
faas-cli list

# Pull Python 3 Flask template
faas-cli template store pull python3-flask

echo "Setup completed successfully!"
