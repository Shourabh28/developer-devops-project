provider "aws" {
  region = "ap-south-1"
}

terraform {
  # This config tells Terraform where to store state
  # backend "local" {}

  backend "s3" {
    bucket = "ap-south-1-flask-project-terraform-state"
    key    = "ap-south-1-flask-project-non-prod/eks/terraform.tfstate"
    region = "ap-south-1"

    dynamodb_table = "ap-south-1-flask-project-terraform-lock-table"
    encrypt        = true
  }
}
