# Kubernetes Operator for MySQL Writer

This project provides a Kubernetes Operator for managing MySQL-related tasks.
It includes Custom Resource Definitions (CRDs), a Python-based Operator, and Docker configurations.

## Overview

Kubernetes CRDs, or Custom Resource Definitions, are like special instructions that help you tell Kubernetes how to handle your unique MySQL-related tasks. This project guides you through creating a Python-based Operator to make interacting with Kubernetes and managing MySQL operations seamless.

## Getting Started

Follow these steps to set up and run the Kubernetes Operator locally:

1. **Create a Kubernetes Cluster:**
   ```bash
   $ cat 00-crd-op-writer.yaml
   # three node (two workers) cluster config
   kind: Cluster
   apiVersion: kind.x-k8s.io/v1alpha4
   name: crd-op-writer
   nodes:
   - role: control-plane
   - role: worker
   - role: worker

   $ kind create cluster --config=00-crd-op-writer.yaml

2. **Define a Kubernetes Namespace:**
kubectl apply -f 01-namespace.yaml

3. **Build and Deploy MySQL::**
cd 02-mysql
kubectl apply -k ./

4. **Deploy the Kubernetes Operator:**
kubectl apply -f 03-sa.yaml
kubectl apply -f 04-crb.yaml
kubectl apply -f 05-crd.yaml

5. **Build the Operator Docker Image:**
cd 06-op-writer-docker
docker build . -t mysql-writer:latest
kind load docker-image mysql-writer:latest --name crd-op-writer

6. **Deploy the Operator:**
kubectl apply -f 07-deployment.yaml

7. **Verify Deployment:**
k get deploy
k get po
k apply -f 08-samples/01-sample.yaml
k get cow
k delete cow sample-client-01

8. **Usage:**
The 06-op-writer-docker directory contains a Python script named clients/mysql.py that serves as the MySQL client. This script establishes a connection to the MySQL database and defines methods for inserting and deleting rows.







