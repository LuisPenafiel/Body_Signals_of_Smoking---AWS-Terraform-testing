# # /terraform/main.tf
# 
# # Proveedor AWS
# provider "aws" {
#   region = var.region
# }
# 
# # Crear un bucket S3 para el dataset y archivos
# resource "aws_s3_bucket" "smoking_data_bucket" {
#   bucket = "smoking-body-signals-data-${var.env}"
#   acl    = "private"
# 
#   tags = {
#     Name        = "SmokingBodySignalsData"
#     Environment = var.env
#   }
# }
# 
# # Subir el dataset al bucket S3
# resource "aws_s3_bucket_object" "smoking_csv" {
#   bucket = aws_s3_bucket.smoking_data_bucket.bucket
#   key    = "data/raw/smoking.csv"
#   source = "../data/raw/smoking.csv"
#   acl    = "private"
# }
# 
# # Subir imágenes al bucket S3 (opcional, para app Streamlit)
# resource "aws_s3_bucket_object" "images" {
#   for_each = fileset("../src/", "*.png")
#   bucket   = aws_s3_bucket.smoking_data_bucket.bucket
#   key      = "src/${each.value}"
#   source   = "../src/${each.value}"
#   acl      = "private"
# }
# 
# # Crear una instancia EC2 para alojar la app Streamlit
# resource "aws_instance" "smoking_app_instance" {
#   ami           = "ami-04e601abe3e1a910f"  # AMI de Ubuntu 22.04 LTS en eu-central-1 (verifica en la consola)
#   instance_type = "t2.micro"               # Gratis en Free Tier
#   key_name      = "smoking-key"            # Crea una clave SSH en AWS si no la tienes
#   security_groups = [aws_security_group.smoking_sg.name]
# 
#   user_data = <<-EOF
#               #!/bin/bash
#               apt-get update -y
#               apt-get install -y python3-pip python3-venv
#               python3 -m venv /home/ubuntu/smoking-env
#               source /home/ubuntu/smoking-env/bin/activate
#               pip install -r /tmp/requirements.txt
#               mkdir -p /home/ubuntu/app
#               cd /home/ubuntu/app
#               aws s3 cp s3://smoking-body-signals-data-${var.env}/data/raw/smoking.csv .
#               aws s3 cp s3://smoking-body-signals-data-${var.env}/src/ . --recursive
#               cp /tmp/app.py .
#               nohup streamlit run app.py --server.port 80 --server.address 0.0.0.0 &
#               EOF
# 
#   tags = {
#     Name        = "SmokingBodySignalsApp"
#     Environment = var.env
#   }
# }
# 
# # Crear un grupo de seguridad para permitir el tráfico HTTP (puerto 80)
# resource "aws_security_group" "smoking_sg" {
#   name        = "smoking-app-sg"
#   description = "Allow HTTP and SSH traffic"
# 
#   ingress {
#     from_port   = 80
#     to_port     = 80
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# 
#   ingress {
#     from_port   = 22
#     to_port     = 22
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]  # Solo para pruebas; limita esto en producción
#   }
# 
#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# 
#   tags = {
#     Name        = "SmokingAppSecurityGroup"
#     Environment = var.env
#   }
# }
# 
# # Opcional: Crear una base de datos RDS para métricas
# resource "aws_db_instance" "smoking_metrics_db" {
#   allocated_storage    = 20
#   engine               = "mysql"
#   engine_version       = "5.7"  # Versión compatible con db.t2.micro en eu-central-1
#   instance_class       = "db.t2.micro"  # Gratis en Free Tier con límites
#   username             = "admin"
#   password             = var.db_password
#   skip_final_snapshot  = true
# 
#   tags = {
#     Name        = "SmokingBodySignalsMetricsDB"
#     Environment = var.env
#   }
# }
# _____________________________________________________________________

terraform {
  backend "remote" {
    organization = "luis-terraform-learning"
    workspaces {
      name = "body-signals-of-smoking"
    }
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.AWS_REGION
}

# Variables (debes tenerlas en variables.tf)
variable "AWS_REGION" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"  # Valor por defecto para Frankfurt
}

variable "env" {
  description = "Environment name (e.g., dev, prod)"
  type        = string
  default     = "dev"
}

variable "AWS_ACCESS_KEY_ID" {
  description = "ID de clave de acceso de AWS"
  type        = string
  sensitive   = true
}

variable "AWS_SECRET_ACCESS_KEY" {
  description = "Clave secreta de acceso de AWS"
  type        = string
  sensitive   = true
}

# VPC básica (los cimientos de tu casa)
resource "aws_vpc" "smoking_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name        = "SmokingVPC-${var.env}"
    Environment = var.env
  }
}

# Subred pública (una habitación con acceso al exterior)
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.smoking_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  tags = {
    Name        = "PublicSubnet-${var.env}"
    Environment = var.env
  }
}

# Puerta al mundo exterior (Internet Gateway)
resource "aws_internet_gateway" "smoking_igw" {
  vpc_id = aws_vpc.smoking_vpc.id
  tags = {
    Name        = "SmokingIGW-${var.env}"
    Environment = var.env
  }
}

# Ruta hacia la puerta (Route Table)
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.smoking_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.smoking_igw.id
  }
  tags = {
    Name        = "PublicRouteTable-${var.env}"
    Environment = var.env
  }
}

# Conectar la habitación con la ruta (Association)
resource "aws_route_table_association" "public_association" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_route_table.id
}