

# Directory structure and their significance

  - This repo consists of below files & folder at root level.<br />
    **(1) Kubernetes :**<br />
        &nbsp;  <> This folder holds all the infra and app level helms charts.<br />
    **(2) rest_api_python_flask :**<br />
        &nbsp;  <> This folder hold the HTTP API code and their unit/integration test cases.<br />
    **(3) terraform :**<br />
        &nbsp;  <> This folder hold the terraform code to create AWS EKS cluster and other infra resources.<br />
    **(4) deploy.sh :**<br />
        &nbsp;  <> This script file needs to be run once and it will create the AWS EKS cluster at one go.<br />

  - Lets go inside each directory now :<br />
    **(1) Kubernetes :**<br />
         |- charts <br />
             |- app <br />
                 |- api                # helm chart to run the stateless flask-app <br />
                 |- database           # helm chart to run statefulSet Database PostgreSQL <br />
             |- common <br />
                 |- aws_lb_controller     # helm chart deploy aws ingress controller <br />
                 |- cert-manager          # helm chart deploy cert-manager on EKS Cluster <br />
                 |- cluster-autoscaler    # helm chart deploy cluster-autoscaler  <br />
                 |- external-dns          # helm chart deploy external-dns <br />

    **(2) rest_api_python_flask :**<br />
         |- Dockerfile               # It creates app logic layer above the base image <br />
         |- docker-compose.yaml      # This can se used for local testing <br />
         |- Jenkinsfile              # CI/CD pipeline to test and deploy the HTTP API service <br />
         |- app.py                   # Actual code logic in written in this file <br />
         |- requirements.txt         # The required modules which needs to be pre-installed <br />
         |- tests                    # Pytest code for integration/unit testing. <br />

    **(3) terraform :**<br />
         |- aws <br />
             |- dev <br />
                 |- vpc.tf             # It does entire network setup with VPC/subnets, etc <br />
                 |- eks.tf             # It creates AWS EKS cluster with 2 Node groups <br />
                 |- eks-iam.tf         # It creates necessary IAM user/roles for EKS <br />
                 |- components-iam.tf  # It create OIDC level roles for EKS components. <br />
             |- uat                    # Empty file for future use <br />
             |- prod                   # Empty file for future use <br />

# Steps to be performed to complete this setup

## Build the base infrastructure using terraform

  ```sh
  $ git clone https://github.com/Shourabh28/developer-devops-project.git
  $ cd ./developer-devops-project
  $ sh deploy.sh dev 
  ```

## Deploy Cluster autoscaler for Node Groups autoscaling using Helm Charts

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

## Deploy Cert-manager for TLS using helm charts

  ```sh
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
  ```

## Deploy External-dns for public and private route53 records using helm charts

  ```sh
  $ cd external-dns
  $ helm repo add bitnami https://charts.bitnami.com/bitnami
  $ helm repo update
  $ helm install external-dns bitnami/external-dns \
        --namespace kube-system \
        -f values.yaml \
        -f values/aws-ap-south-1-dev.yaml
  $ cd ../
  ```

## Deploy AWS Load Balancer Controller for ingress using helm charts

  ```sh
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
  ```

## Deploy PostgresSQL Database as a StatefulSets using helm charts

  ```sh
  $ cd ../app/database
  $ kubectl create namespace dev
  $ helm install postgresql . \
        --namespace dev \
        -f values.yaml \
        -f values/aws-ap-south-1-dev.yaml
  $ cd ../
  ```

## Deploy flask-app with fluentd as sidecar using helm charts

  ```sh
  $ cd ../../../rest_api_python_flask
  $ docker build -t flask_msg_app:0.2.5 .
  $ cd ../kubernetes/charts/app/api
  $ helm install flask-app . \
        --namespace dev \
        -f values.yaml \
        -f values/aws-ap-south-1-dev.yaml 
  ```
