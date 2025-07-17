#!/bin/bash
sudo apt update -y
sudo apt install python3-pip git -y
git clone https://github.com/LuisPenafiel/Body_Signals_of_Smoking---AWS-Terraform-testing.git
cd Body_Signals_of_Smoking---AWS-Terraform-testing
pip3 install -r requirements.txt
cd src
export AWS_REGION=eu-central-1
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
