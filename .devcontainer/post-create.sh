#!/bin/bash

# Actualizar el sistema
sudo apt-get update -y

# Instalar AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf awscliv2.zip aws

# Verificar que AWS CLI esté instalado
aws --version