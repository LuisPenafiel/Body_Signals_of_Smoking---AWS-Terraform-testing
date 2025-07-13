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

# main.tf

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

  # Permitir Streamlit (puerto 8501, para pruebas)
  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Para pruebas; limita a tu IP en prod
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

# S3 Bucket for app files and DB
resource "aws_s3_bucket" "smoking_data_dev" {
  bucket = "smoking-body-signals-data-dev"
  tags = {
    Name        = "Smoking Body Signals Data Dev"
    Environment = var.env
  }
}

# Deshabilitar Block Public Access para permitir policy
resource "aws_s3_bucket_public_access_block" "smoking_data_dev_block" {
  bucket = aws_s3_bucket.smoking_data_dev.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# Policy para acceso público de lectura (GetObject)
resource "aws_s3_bucket_policy" "smoking_data_dev_policy" {
  bucket = aws_s3_bucket.smoking_data_dev.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.smoking_data_dev.arn}/*"
      }
    ]
  })

  depends_on = [aws_s3_bucket_public_access_block.smoking_data_dev_block]
}

# SSH Key Pair (genera .pem automáticamente, pero descarga manual desde AWS)
resource "aws_key_pair" "smoking_key" {
  key_name   = var.key_name
  public_key = var.ec2_public_key  # Usa variable de TF Cloud
}

resource "aws_instance" "smoking_app_dev" {
  ami           = "ami-0dc33c9c954b3f073"  # AMI Ubuntu 22.04 LTS en eu-central-1 (de tu CLI)
  instance_type = var.instance_type
  key_name      = aws_key_pair.smoking_key.key_name
  vpc_security_group_ids = [aws_security_group.smoking_sg.id]
  subnet_id     = module.vpc.public_subnets[0]
  associate_public_ip_address = true  # Añadido para public DNS/IP

  user_data = base64encode(<<EOF
#!/bin/bash
sudo apt update -y
sudo apt install python3-pip git -y
pip3 install streamlit pandas scikit-learn boto3 pillow
git clone https://github.com/LuisPenafiel/Body_Signals_of_Smoking---AWS-Terraform-testing.git
cd Body_Signals_of_Smoking---AWS-Terraform-testing/src
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
EOF
  )

  tags = {
    Name        = "SmokingAppDev"
    Environment = var.env
  }
}

# Output para DNS público
output "ec2_public_dns" {
  value = aws_instance.smoking_app_dev.public_dns
}