#!/bin/bash

# Script para subir archivos esenciales de src/ a S3
# Uso: ./upload_to_s3.sh
# Requisitos: AWS CLI configurado con credenciales

BUCKET="smoking-body-signals-data-dev"  # Nombre del bucket
SRC_PATH="../src/"  # Path relativo a src/ (ajusta si necesario)
FILES=(  # Lista de archivos a subir (añade/quita según necesites)
  "random_forest_model_Default.pkl"
  "scaler.pkl"
  "body.jpg"
  "Gender_smoking.png"
  "GTP.png"
  "hemoglobine_gender.png"  # Ajusta si se llama hemoglobin_gender.png
  "Triglyceride.png"
)

# Loop para subir cada archivo
for FILE in "${FILES[@]}"; do
  LOCAL_FILE="${SRC_PATH}${FILE}"
  
  # Check si el archivo existe localmente
  if [ ! -f "$LOCAL_FILE" ]; then
    echo "Error: Archivo no encontrado: $LOCAL_FILE. Saltando."
    continue
  fi
  
  # Subir a S3 en el path src/
  aws s3 cp "$LOCAL_FILE" s3://$BUCKET/src/
  if [ $? -eq 0 ]; then
    echo "Subido exitosamente: $FILE"
  else
    echo "Error subiendo $FILE. Revisa AWS CLI."
  fi
done

echo "Subida completada."