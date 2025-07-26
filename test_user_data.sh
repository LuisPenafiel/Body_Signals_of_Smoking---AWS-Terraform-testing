#!/bin/bash
sudo apt update -y
sudo apt install python3-pip git awscli net-tools -y  # Add awscli/net-tools if not already
cd /home/ubuntu/Body_Signals_of_Smoking---AWS-Terraform-testing/src # 
mkdir -p Body_Signals_of_Smoking---AWS-Terraform-testing/src
aws s3 sync s3://smoking-body-signals-data-dev/src/ Body_Signals_of_Smoking---AWS-Terraform-testing/src/ --quiet  # If testing in Codespaces, assume AWS creds set
cd Body_Signals_of_Smoking---AWS-Terraform-testing
pip3 install -r requirements.txt --no-cache-dir
cd src
export AWS_REGION=eu-central-1
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true &

# To Run if errors in ssh ubuntu and main.tf user --- ./test_user_data.sh