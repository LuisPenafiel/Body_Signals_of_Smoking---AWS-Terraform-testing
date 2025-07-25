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
    CostCenter  = "smoking-research"
    AutoDelete  = "true"
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
    cidr_blocks = ["0.0.0.0/0"]  # Temporary; replace with your IP for security
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

resource "aws_s3_bucket_lifecycle_configuration" "data_cleanup" {
  bucket = aws_s3_bucket.smoking_data_dev.id

  rule {
    id     = "auto-delete"
    status = "Enabled"
    expiration {
      days = 30  # Delete files after 30 days
    }
  }
}

resource "aws_s3_bucket_policy" "smoking_data_dev_policy" {
  bucket = aws_s3_bucket.smoking_data_dev.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = {"AWS": aws_iam_role.ec2_s3_role.arn}
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.smoking_data_dev.arn}/src/*"
      }
    ]
  })
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

  instance_market_options {
    market_type = "spot"
    spot_options {
      max_price = "0.003"  # 50% of on-demand price for t2.micro
    }
  }

  user_data = base64encode(<<EOF
  #!/bin/bash
  set -x
  sudo apt update -y
  sudo apt install -y python3-pip git awscli net-tools
  cd /home/ubuntu
  git clone --depth=1 https://github.com/LuisPenafiel/Body_Signals_of_Smoking---AWS-Terraform-testing.git
  cd /home/ubuntu/Body_Signals_of_Smoking---AWS-Terraform-testing/src
  aws s3 sync s3://smoking-body-signals-data-dev/src/ ./
  if [ $? -ne 0 ]; then echo "S3 sync failed at $(date)" >> /home/ubuntu/sync_error.log; exit 1; fi
  pip3 install -r requirements.txt --no-cache-dir || { echo "Pip install failed at $(date)" >> /home/ubuntu/install_error.log; exit 1; }
  export AWS_REGION=eu-central-1
  # Comment out auto-shutdown for persistent web
  # echo '#!/bin/bash\nsleep 3600\nif ! who | grep -q pts; then\n  shutdown -h now\nfi' > /home/ubuntu/auto-shutdown.sh
  # chmod +x /home/ubuntu/auto-shutdown.sh
  # nohup /home/ubuntu/auto-shutdown.sh &
  nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true --logger.level debug > /home/ubuntu/streamlit.log 2>&1 &
  sleep 10
  if ! pgrep -f streamlit > /dev/null; then
    echo "Streamlit failed to start at $(date). Check logs:" >> /home/ubuntu/streamlit.log
    cat /home/ubuntu/streamlit.log >> /home/ubuntu/streamlit.log
  fi
  echo "Streamlit started at $(date) with PID $$ at http://18.198.181.6:8501" >> /home/ubuntu/streamlit.log
  netstat -tuln >> /home/ubuntu/network_check.log 2>&1
  EOF
  )

  disable_api_termination = false
  tags = {
    Name        = "SmokingAppDev"
    Environment = var.env
    CostCenter  = "smoking-research"
    AutoDelete  = "true"
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
      Action   = ["s3:GetObject", "s3:ListBucket"]
      Resource = ["${aws_s3_bucket.smoking_data_dev.arn}", "${aws_s3_bucket.smoking_data_dev.arn}/src/*"]
    }]
  })
}

resource "aws_iam_instance_profile" "ec2_s3_profile" {
  name = "ec2_s3_profile"
  role = aws_iam_role.ec2_s3_role.name
}