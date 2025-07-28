#!/bin/bash

MY_IP=$(curl -s ifconfig.me)
SECURITY_GROUP_ID=sg-0d6bd9f0b254d3442  # Reemplaza con tu ID real (ver abajo cómo encontrarlo)
REGION=eu-central-1

# Revoca accesos anteriores para limpiar (opcional)
aws ec2 revoke-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 22 --cidr 0.0.0.0/0 --region $REGION

# Añade la IP actual
aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 22 --cidr "$MY_IP/32" --region $REGION

echo "IP actualizada a $MY_IP/32 en el Security Group."