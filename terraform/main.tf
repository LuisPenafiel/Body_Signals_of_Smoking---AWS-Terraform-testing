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
      version = "~> 5.30.0"
    }
  }
}

provider "aws" {
  region     = var.AWS_REGION
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.8.0"

  name = "smoking-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.AWS_REGION}a", "${var.AWS_REGION}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway                   = false
  enable_vpn_gateway                   = false
  enable_network_address_usage_metrics = var.enable_network_address_usage_metrics

  tags = {
    Environment = var.env
  }
}

resource "aws_security_group" "smoking_sg" {
  name        = "smoking-app-sg-${var.env}"
  description = "Security group for Smoking App"
  vpc_id      = module.vpc.vpc_id

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
    cidr_blocks = ["0.0.0.0/0"]  # Revertido temporalmente para permitir SSH desde cualquier IP
  }

  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

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

resource "aws_s3_bucket" "smoking_data_dev" {
  bucket = "smoking-body-signals-data-dev"
  tags = {
    Name        = "Smoking Body Signals Data Dev"
    Environment = var.env
  }
}

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
}

resource "aws_key_pair" "smoking_key" {
  key_name   = var.key_name
  public_key = var.ec2_public_key
}

resource "aws_instance" "smoking_app_dev" {
  ami                         = "ami-0dc33c9c954b3f073"  # Ubuntu 22.04 LTS, actualizado 2025-07-12
  instance_type               = var.instance_type
  key_name                    = aws_key_pair.smoking_key.key_name
  vpc_security_group_ids      = [aws_security_group.smoking_sg.id]
  subnet_id                   = module.vpc.public_subnets[0]
  associate_public_ip_address = true
  iam_instance_profile        = aws_iam_instance_profile.ec2_s3_profile.name

  user_data = base64encode(<<EOF
#!/bin/bash
set -e  # Exit on error
LOG_FILE=/home/ubuntu/setup.log
echo "Starting setup at $(date)" > $LOG_FILE 2>&1
sudo apt update -y >> $LOG_FILE 2>&1
sudo apt install -y python3-pip git awscli net-tools >> $LOG_FILE 2>&1
pip3 install --upgrade pip >> $LOG_FILE 2>&1
cd /home/ubuntu
mkdir -p Body_Signals_of_Smoking---AWS-Terraform-testing/src
cd Body_Signals_of_Smoking---AWS-Terraform-testing/src
aws s3 sync s3://smoking-body-signals-data-dev/src/ . --quiet >> $LOG_FILE 2>&1
if [ $? -ne 0 ]; then
  echo "S3 sync failed at $(date)" >> $LOG_FILE
  exit 1
fi
pip3 install -r requirements.txt --no-cache-dir >> $LOG_FILE 2>&1 || {
  echo "Pip install failed at $(date)" >> $LOG_FILE
  exit 1
}
export AWS_REGION=eu-central-1
export AWS_DEFAULT_REGION=eu-central-1
# Start Streamlit with health check
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true --logger.level debug > /home/ubuntu/streamlit.log 2>&1 &
sleep 5
if pgrep -f streamlit > /dev/null; then
  PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
  echo "Streamlit started at $(date) with PID $(pgrep -f streamlit) at http://$PUBLIC_IP:8501" >> $LOG_FILE
else
  echo "Streamlit failed to start at $(date). Check logs." >> $LOG_FILE
  cat /home/ubuntu/streamlit.log >> $LOG_FILE
  exit 1
fi
netstat -tuln >> /home/ubuntu/network_check.log 2>&1
echo "Setup complete at $(date)" >> $LOG_FILE
# Optional auto-shutdown (comment out if not desired)
# echo '#!/bin/bash\nwhile true; do\n  sleep 21600\n  if ! who | grep -q pts; then\n    shutdown -h now\n  fi\ndone' > /home/ubuntu/auto-shutdown.sh
# chmod +x /home/ubuntu/auto-shutdown.sh
# nohup /home/ubuntu/auto-shutdown.sh &
EOF
  )

  tags = {
    Name        = "SmokingAppDev"
    Environment = var.env
  }
}

resource "aws_eip" "smoking_eip" {
  instance = aws_instance.smoking_app_dev.id
  domain   = "vpc"
  tags = {
    Name        = "SmokingAppEIP"
    Environment = var.env
  }
}

output "ec2_public_ip" {
  value = aws_eip.smoking_eip.public_ip
}

resource "aws_iam_role" "ec2_s3_role" {
  name = "ec2_s3_read_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "ec2_s3_extended" {
  name   = "ec2_s3_extended_policy"
  role   = aws_iam_role.ec2_s3_role.name
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:Get*", "s3:List*"]
      Resource = "*"
    }]
  })
}

resource "aws_iam_instance_profile" "ec2_s3_profile" {
  name = "ec2_s3_profile"
  role = aws_iam_role.ec2_s3_role.name
}