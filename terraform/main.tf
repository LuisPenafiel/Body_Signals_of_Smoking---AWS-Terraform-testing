# /terraform/main.tf

# Proveedor AWS
provider "aws" {
  region = var.region
}

# Crear un bucket S3 para el dataset y archivos
resource "aws_s3_bucket" "smoking_data_bucket" {
  bucket = "smoking-body-signals-data-${var.env}"
  acl    = "private"

  tags = {
    Name        = "SmokingBodySignalsData"
    Environment = var.env
  }
}

# Subir el dataset al bucket S3
resource "aws_s3_bucket_object" "smoking_csv" {
  bucket = aws_s3_bucket.smoking_data_bucket.bucket
  key    = "data/raw/smoking.csv"
  source = "../data/raw/smoking.csv"
  acl    = "private"
}

# Subir imágenes al bucket S3 (opcional, para app Streamlit)
resource "aws_s3_bucket_object" "images" {
  for_each = fileset("../src/", "*.png")
  bucket   = aws_s3_bucket.smoking_data_bucket.bucket
  key      = "src/${each.value}"
  source   = "../src/${each.value}"
  acl      = "private"
}

# Crear una instancia EC2 para alojar la app Streamlit
resource "aws_instance" "smoking_app_instance" {
  ami           = "ami-0c55b159cbfafe1f0"  # Ubuntu 24.04 LTS en eu-central-1 (verifica la AMI más reciente)
  instance_type = "t2.micro"               # Gratis en Free Tier
  key_name      = "smoking-key"            # Crea una clave SSH en AWS si no la tienes
  security_groups = [aws_security_group.smoking_sg.name]

  user_data = <<-EOF
              #!/bin/bash
              apt-get update -y
              apt-get install -y python3-pip python3-venv
              python3 -m venv /home/ubuntu/smoking-env
              source /home/ubuntu/smoking-env/bin/activate
              pip install -r /tmp/requirements.txt
              mkdir -p /home/ubuntu/app
              cd /home/ubuntu/app
              aws s3 cp s3://smoking-body-signals-data-${var.env}/data/raw/smoking.csv .
              aws s3 cp s3://smoking-body-signals-data-${var.env}/src/ . --recursive
              cp /tmp/app.py .
              nohup streamlit run app.py --server.port 80 --server.address 0.0.0.0 &
              EOF

  tags = {
    Name        = "SmokingBodySignalsApp"
    Environment = var.env
  }
}

# Crear un grupo de seguridad para permitir el tráfico HTTP (puerto 80)
resource "aws_security_group" "smoking_sg" {
  name        = "smoking-app-sg"
  description = "Allow HTTP and SSH traffic"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Solo para pruebas; limita esto en producción
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "SmokingAppSecurityGroup"
    Environment = var.env
  }
}

# Opcional: Crear una base de datos RDS para métricas
resource "aws_db_instance" "smoking_metrics_db" {
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t2.micro"  # Gratis en Free Tier con límites
  username             = "admin"
  password             = var.db_password
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true

  tags = {
    Name        = "SmokingBodySignalsMetricsDB"
    Environment = var.env
  }
}
