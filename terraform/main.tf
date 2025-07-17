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
  region = var.AWS_REGION
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
    cidr_blocks = ["0.0.0.0/0"]
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

resource "aws_s3_bucket_public_access_block" "smoking_data_dev_block" {
  bucket = aws_s3_bucket.smoking_data_dev.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
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

  depends_on = [aws_s3_bucket_public_access_block.smoking_data_dev_block]
}

resource "aws_key_pair" "smoking_key" {
  key_name   = var.key_name
  public_key = var.ec2_public_key
}

resource "aws_instance" "smoking_app_dev" {
  ami                         = "ami-05b91990f4b2d588f"
  instance_type               = var.instance_type
  key_name                    = aws_key_pair.smoking_key.key_name
  vpc_security_group_ids      = [aws_security_group.smoking_sg.id]
  subnet_id                   = module.vpc.public_subnets[0]
  associate_public_ip_address = true
  iam_instance_profile        = aws_iam_instance_profile.ec2_s3_profile.name

  user_data = base64encode(<<EOF
  #!/bin/bash
  sudo apt update -y
  sudo apt install -y python3-pip git awscli net-tools
  cd /home/ubuntu
  mkdir -p Body_Signals_of_Smoking---AWS-Terraform-testing
  git clone https://github.com/LuisPenafiel/Body_Signals_of_Smoking---AWS-Terraform-testing.git .
  cd src
  pip3 install -r requirements.txt || { echo "Pip install failed at $(date)" >> /home/ubuntu/install_error.log; exit 1; }
  export AWS_REGION=eu-central-1
  nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > /home/ubuntu/streamlit.log 2>&1 &
  echo "Streamlit started at $(date) with PID $$ at http://18.198.181.6:8501" >> /home/ubuntu/streamlit.log
  netstat -tuln >> /home/ubuntu/network_check.log 2>&1
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

resource "aws_cloudwatch_metric_alarm" "cpu_alarm" {
  alarm_name          = "ec2-cpu-alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors ec2 cpu utilization exceeding 80%"
  alarm_actions       = []
  dimensions = {
    InstanceId = aws_instance.smoking_app_dev.id
  }
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
      Action   = ["s3:*", "ec2:CreateImage"]
      Resource = "*"
    }]
  })
}

resource "aws_iam_instance_profile" "ec2_s3_profile" {
  name = "ec2_s3_profile"
  role = aws_iam_role.ec2_s3_role.name
}