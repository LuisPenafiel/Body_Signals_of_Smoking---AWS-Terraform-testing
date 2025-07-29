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
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # For HTTPS
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Abierto temporalmente
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

resource "aws_launch_configuration" "smoking_lc" {
  name_prefix          = "smoking-lc-"
  image_id             = "ami-0dc33c9c954b3f073" # Confirmada como válida por tu comando
  instance_type        = var.instance_type
  key_name             = aws_key_pair.smoking_key.key_name
  security_groups      = [aws_security_group.smoking_sg.id]
  iam_instance_profile = aws_iam_instance_profile.ec2_s3_profile.name

  user_data = base64encode(<<-EOF
    #!/bin/bash
    set -e
    LOG_FILE="/home/ubuntu/setup.log"
    echo "Starting setup at $(date)" > "$LOG_FILE" 2>&1
    sudo apt update -y >> "$LOG_FILE" 2>&1 || { echo "apt update failed"; exit 1; }
    sudo apt install -y python3-pip git awscli net-tools >> "$LOG_FILE" 2>&1 || { echo "apt install failed"; exit 1; }
    pip3 install --upgrade pip >> "$LOG_FILE" 2>&1 || { echo "pip upgrade failed"; exit 1; }
    cd /home/ubuntu || { echo "cd failed"; exit 1; }
    mkdir -p Body_Signals_of_Smoking---AWS-Terraform-testing/src
    cd Body_Signals_of_Smoking---AWS-Terraform-testing/src || { echo "cd src failed"; exit 1; }
    aws s3 sync s3://smoking-body-signals-data-dev/src/ . --quiet >> "$LOG_FILE" 2>&1 || { echo "S3 sync failed"; exit 1; }
    pip3 install -r requirements.txt --no-cache-dir >> "$LOG_FILE" 2>&1 || { echo "pip install failed"; exit 1; }
    export AWS_REGION=eu-central-1
    export AWS_DEFAULT_REGION=eu-central-1
    nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true --logger.level debug > /home/ubuntu/streamlit.log 2>&1 &
    sleep 5
    if pgrep -f streamlit > /dev/null; then
      PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
      echo "Streamlit started at $(date) with PID $(pgrep -f streamlit) at http://$PUBLIC_IP:8501" >> "$LOG_FILE"
    else
      echo "Streamlit failed to start at $(date). Check logs." >> "$LOG_FILE"
      cat /home/ubuntu/streamlit.log >> "$LOG_FILE"
      exit 1
    fi
    netstat -tuln >> /home/ubuntu/network_check.log 2>&1
    echo "Setup complete at $(date)" >> "$LOG_FILE"
  EOF
  )

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "smoking_asg" {
  name                 = "smoking-asg"
  launch_configuration = aws_launch_configuration.smoking_lc.name
  min_size             = 1
  max_size             = 2
  desired_capacity     = 1
  vpc_zone_identifier  = module.vpc.public_subnets
  target_group_arns    = [aws_lb_target_group.smoking_tg.arn]

  tag {
    key                 = "Name"
    value               = "SmokingASGInstance"
    propagate_at_launch = true
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_policy" "smoking_scale_out" {
  name                   = "smoking-scale-out"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.smoking_asg.name
}

resource "aws_autoscaling_policy" "smoking_scale_in" {
  name                   = "smoking-scale-in"
  scaling_adjustment     = -1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.smoking_asg.name
}

resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name          = "high-cpu-alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 60
  statistic           = "Average"
  threshold           = 60
  alarm_description   = "Scale out if CPU > 60%"
  alarm_actions       = [aws_autoscaling_policy.smoking_scale_out.arn]
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.smoking_asg.name
  }
}

resource "aws_cloudwatch_metric_alarm" "low_cpu" {
  alarm_name          = "low-cpu-alarm"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 60
  statistic           = "Average"
  threshold           = 30
  alarm_description   = "Scale in if CPU < 30%"
  alarm_actions       = [aws_autoscaling_policy.smoking_scale_in.arn]
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.smoking_asg.name
  }
}

resource "aws_lb" "smoking_alb" {
  name               = "smoking-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.smoking_sg.id]
  subnets            = module.vpc.public_subnets

  enable_deletion_protection = false

  tags = {
    Name        = "SmokingALB"
    Environment = var.env
  }
}

resource "aws_lb_target_group" "smoking_tg" {
  name     = "smoking-tg"
  port     = 8501
  protocol = "HTTP"
  vpc_id   = module.vpc.vpc_id

  health_check {
    path     = "/"
    protocol = "HTTP"
    matcher  = "200"
    interval = 30
    timeout  = 5
  }

  tags = {
    Name        = "SmokingTG"
    Environment = var.env
  }
}

resource "aws_lb_listener" "smoking_http" {
  load_balancer_arn = aws_lb.smoking_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_lb_listener" "smoking_https" {
  load_balancer_arn = aws_lb.smoking_alb.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = aws_acm_certificate.smoking_cert.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.smoking_tg.arn
  }
}

resource "aws_acm_certificate" "smoking_cert" {
  domain_name       = "smoking-body-signals.luispenafiel.com" # Reemplaza con tu dominio
  validation_method = "DNS"

  tags = {
    Name        = "SmokingCert"
    Environment = var.env
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_zone" "smoking_zone" {
  name = "luispenafiel.com" # Reemplaza con tu dominio base

  tags = {
    Environment = var.env
  }
}

resource "aws_route53_record" "smoking_cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.smoking_cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = aws_route53_zone.smoking_zone.zone_id
}

resource "aws_acm_certificate_validation" "smoking_cert_validation" {
  certificate_arn         = aws_acm_certificate.smoking_cert.arn
  validation_record_fqdns = [for record in aws_route53_record.smoking_cert_validation : record.fqdn]
}

resource "aws_route53_record" "smoking_a" {
  zone_id = aws_route53_zone.smoking_zone.zone_id
  name    = "smoking-body-signals.luispenafiel.com" # Reemplaza con tu subdomain
  type    = "A"

  alias {
    name                   = aws_lb.smoking_alb.dns_name
    zone_id                = aws_lb.smoking_alb.zone_id
    evaluate_target_health = true
  }
}

resource "aws_eip" "smoking_eip" {
  domain = "vpc"
  tags = {
    Name        = "SmokingAppEIP"
    Environment = var.env
  }
}

output "ec2_public_ip" {
  value = aws_eip.smoking_eip.public_ip
}

output "alb_dns_name" {
  value = aws_lb.smoking_alb.dns_name
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
  name = "ec2_s3_extended_policy"
  role = aws_iam_role.ec2_s3_role.name
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