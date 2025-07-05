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

# Instalar Terraform (versión reciente: 1.9.5 como ejemplo, ajusta según necesites)
echo "Installing Terraform"
wget -P /tmp https://releases.hashicorp.com/terraform/1.9.5/terraform_1.9.5_linux_amd64.zip
unzip /tmp/terraform_1.9.5_linux_amd64.zip -d /tmp
sudo mv /tmp/terraform /usr/local/bin/
rm -f /tmp/terraform_1.9.5_linux_amd64.zip

# Verificar que Terraform esté instalado
terraform --version