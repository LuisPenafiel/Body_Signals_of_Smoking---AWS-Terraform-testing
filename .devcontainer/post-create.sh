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

# Instalar dependencias GLOBALMENTE con sudo
echo "Instalando dependencias de Python GLOBALMENTE"
sudo pip3 install --no-cache-dir \
    streamlit==1.46.1 \
    pandas==2.3.1 \
    numpy==1.26.0 \
    scikit-learn==1.4.1.post1 \
    boto3==1.39.3 \
    mysql-connector-python==9.3.0 \
    pillow==11.3.0

# Añadir .local/bin al PATH (por si acaso)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verificaciones MEJORADAS
echo "--- Versiones instaladas ---"
python3 --version
pip3 --version
echo "Streamlit: $(streamlit --version)"
echo "pandas: $(python3 -c "import pandas as pd; print(pd.__version__)")"
echo "numpy: $(python3 -c "import numpy as np; print(np.__version__)")"
echo "scikit-learn: $(python3 -c "import sklearn; print(sklearn.__version__)")"
echo "boto3: $(python3 -c "import boto3; print(boto3.__version__)")"
echo "MySQL Connector: $(python3 -c "import mysql.connector; print(mysql.connector.__version__)")"
echo "Pillow: $(python3 -c "from PIL import __version__; print(__version__)")"