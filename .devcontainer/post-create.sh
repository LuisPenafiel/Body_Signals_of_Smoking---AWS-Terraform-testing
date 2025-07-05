#!/bin/bash

# Actualizar el sistema (no interactivo)
sudo apt-get update -y

# Instalar AWS CLI (no interactivo)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip -o awscliv2.zip  # -o fuerza la sobrescritura sin preguntar
sudo ./aws/install --update  # --update asegura instalación sin interacción
rm -rf awscliv2.zip aws

# Verificar que AWS CLI esté instalado
aws --version

# Instalar Terraform (versión 1.12.2, no interactivo)
echo "Installing Terraform"
wget -P /tmp https://releases.hashicorp.com/terraform/1.12.2/terraform_1.12.2_linux_amd64.zip -q  # -q para silenciar salida
unzip -o /tmp/terraform_1.12.2_linux_amd64.zip -d /tmp  # -o fuerza la descompresión
sudo mv /tmp/terraform /usr/local/bin/  # Mueve sin pedir confirmación
rm -f /tmp/terraform_1.12.2_linux_amd64.zip

# Verificar que Terraform esté instalado
terraform --version