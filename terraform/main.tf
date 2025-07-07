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
      version = "~> 5.30.0"  # Upgraded to 5.x series
    }
  }
}

provider "aws" {
  region = var.AWS_REGION
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.8.0"  # Keep this version

  name = "smoking-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.AWS_REGION}a", "${var.AWS_REGION}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway     = false
  enable_vpn_gateway     = false
  enable_network_address_usage_metrics = var.enable_network_address_usage_metrics

  tags = {
    Environment = var.env
  }
}
resource "aws_security_group" "smoking_sg" {
  name        = "smoking-app-sg-${var.env}"
  description = "Security group for Smoking App"
  vpc_id      = module.vpc.vpc_id

  # Permitir tráfico HTTP (puerto 80)
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Para pruebas; limita en producción
  }

  # Permitir SSH (puerto 22, solo para pruebas)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Limita en producción a tu IP
  }

  # Permitir todo el tráfico saliente
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "SmokingAppSG-${var.env}"
    Environment = var.env
  }
}