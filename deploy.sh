#!/bin/bash

ENV=$1

###### Creating terraform pre-requisites for AWS using AWS CLI commands ######

# S3 bucket with encryption to store terraform statefiles
aws s3api create-bucket --bucket ap-south-1-flask-project-terraform-state --region ap-south-1
aws s3api put-bucket-encryption --bucket ap-south-1-flask-project-terraform-state --server-side-encryption-configuration "{\"Rules\": [{\"ApplyServerSideEncryptionByDefault\":{\"SSEAlgorithm\": \"AES256\"}}]}" --region ap-south-1

# Creating DynamoDB Table to utilize terraform lock mechanism
aws dynamodb create-table --table-name ap-south-1-flask-project-terraform-lock-table --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 --region ap-south-1


###### Get the environment details ######
ENV=$1

if [ $ENV == 'dev' ]
then
   cd ./terraform/aws/dev
   echo "You are in Dev Environment"
elif [ $ENV == 'uat' ]
then
   cd ./terraform/aws/uat
   echo "You are in UAT Environment"
elif [ $ENV == 'prod' ]
then
   cd ./terraform/aws/prod
   echo "You are in Prod Environment"
else
    echo "Please pass correct Environment name. Options are dev, uat or prod"
fi

###### Deploy the terraform code to setup the K8s Cluster ######
terraform init
terraform plan -out out.terraform
terraform apply out.terraform
rm out.terraform
