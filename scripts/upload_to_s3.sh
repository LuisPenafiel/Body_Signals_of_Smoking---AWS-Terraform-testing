#!/bin/bash

# Script para subir archivos esenciales de src/ a S3
# Uso: ./scripts/upload_to_s3.sh
# Requisitos: AWS CLI configurado con credenciales

BUCKET="smoking-body-signals-data-dev"
SRC_PATH="/workspaces/Body_Signals_of_Smoking---AWS-Terraform-testing/src/"  # Absolute path for Codespaces
FILES=(
  "random_forest_model_Default.pkl"
  "scaler.pkl"
  "body.jpg"
  "Gender_smoking.png"
  "GTP.png"
  "hemoglobine_gender.png" 
  "Triglyceride.png"
  "requirements.txt"
)

# Check AWS CLI configuration
if ! aws sts get-caller-identity >/dev/null 2>&1; then
  echo "Error: AWS CLI not configured. Set credentials first."
  exit 1
fi

# Loop para subir cada archivo
for FILE in "${FILES[@]}"; do
  LOCAL_FILE="${SRC_PATH}${FILE}"
  
  # Check si el archivo existe localmente
  if [ ! -f "$LOCAL_FILE" ]; then
    echo "Error: Archivo no encontrado: $LOCAL_FILE. Saltando."
    continue
  fi
  
  # Subir a S3 en el path src/
  aws s3 cp "$LOCAL_FILE" s3://$BUCKET/src/ --quiet
  if [ $? -eq 0 ]; then
    echo "Subido exitosamente: $FILE"
  else
    echo "Error subiendo $FILE. Revisa AWS CLI o permisos."
  fi
done

echo "Subida completada."

# To Run --- ./scripts/upload_to_s3.sh