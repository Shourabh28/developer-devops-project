
NOTE: 

## Directory structure and their significance

  - This repo consists of below files & folder at root level.
    **(1) Kubernetes :**
        <> This folder holds all the infra and app level helms charts.
    **(2) rest_api_python_flask :**
        <> This folder hold the HTTP API code and their unit/integration test cases.
    **(3) terraform :**
        <> This folder hold the terraform code to create AWS EKS cluster and other infra resources.
    **(4) deploy.sh :**
        <> This script file needs to be run once and it will create the AWS EKS cluster at one go.

  - Lets go inside each directory now :
    **(1) Kubernetes :**
         |- charts 
             |- app
                 |- api                # helm chart to run the stateless flask-app
                 |- database           # helm chart to run statefulSet Database PostgreSQL
             |- common 
                 |- aws_lb_controller     # helm chart deploy aws ingress controller
                 |- cert-manager          # helm chart deploy cert-manager on EKS Cluster
                 |- cluster-autoscaler    # helm chart deploy cluster-autoscaler 
                 |- external-dns          # helm chart deploy external-dns

    **(2) rest_api_python_flask :**
         |- Dockerfile               # It creates app logic layer above the base image
         |- docker-compose.yaml      # This can se used for local testing
         |- Jenkinsfile              # CI/CD pipeline to test and deploy the HTTP API service
         |- app.py                   # Actual code logic in written in this file
         |- requirements.txt         # The required modules which needs to be pre-installed
         |- tests                    # Pytest code for integration/unit testing.

    **(3) terraform :**
         |- aws
             |- dev
                 |- vpc.tf             # It does entire network setup with VPC/subnets, etc
                 |- eks.tf             # It creates AWS EKS cluster with 2 Node groups
                 |- eks-iam.tf         # It creates necessary IAM user/roles for EKS
                 |- components-iam.tf  # It create OIDC level roles for EKS components.
             |- uat                    # Empty file for future use
             |- prod                   # Empty file for future use

## Steps to be performed to complete this setup

# Build the base infrastructure using terraform

  ```sh
  $ git clone https://github.com/Shourabh28/developer-devops-project.git
  $ cd ./developer-devops-project
  $ sh deploy.sh dev 
  ```

# Deploy Cluster autoscaler for Node Groups autoscaling using Helm Charts

  ```sh
  $ cd kubernetes/charts/common/
  $ cd cluster-autoscaler
  $ helm repo add autoscaler https://kubernetes.github.io/autoscaler
  $ helm repo update
  $ helm upgrade --install cluster-autoscaler autoscaler/cluster-autoscaler \
        --namespace kube-system \
        -f values.yaml \
        -f values/eks-ap-south-1-dev.yaml
  $ cd ../
  ```

# Deploy Cert-manager for TLS using helm charts

  $ cd cert-manager
  $ kubectl create ns cert-manager
  $ helm repo add jetstack https://charts.jetstack.io
  $ helm repo update
  $ helm upgrade --install cert-manager jetstack/cert-manager \
        --namespace cert-manager \
        --create-namespace \
        -f values.yaml \
        -f values/aws-ap-south-1-dev.yaml
  $ cd ../

# Deploy External-dns for public and private route53 records using helm charts

  $ cd external-dns
  $ helm repo add bitnami https://charts.bitnami.com/bitnami
  $ helm repo update
  $ helm install external-dns bitnami/external-dns \
        --namespace kube-system \
        -f values.yaml \
        -f values/aws-ap-south-1-dev.yaml
  $ cd ../

# Deploy AWS Load Balancer Controller for ingress using helm charts

  $ cd aws_lb_controller
  $ helm repo add eks https://aws.github.io/eks-charts
  $ kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"
  $ helm repo update
  $ helm install aws-load-balancer-controller \
        eks/aws-load-balancer-controller \
        --namespace kube-system \
        -f values.yaml \
        -f values/aws-ap-south-1-dev.yaml
  $ cd ../

# Deploy PostgresSQL Database as a StatefulSets using helm charts

  $ cd ../app/database
  $ kubectl create namespace dev
  $ helm install postgresql . \
        --namespace dev \
        -f values.yaml \
        -f values/aws-ap-south-1-dev.yaml
  $ cd ../

# Deploy flask-app with fluentd as sidecar using helm charts

  $ cd ../../../rest_api_python_flask
  $ docker build -t flask_msg_app:0.2.5 .
  $ cd ../kubernetes/charts/app/api
  $ helm install flask-app . \
        --namespace dev \
        -f values.yaml \
        -f values/aws-ap-south-1-dev.yaml 

