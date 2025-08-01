variable "AWS_REGION" {
  description = "The AWS region where resources will be created (e.g., eu-central-1)"
  type        = string
  default     = "eu-central-1"
  validation {
    condition     = can(regex("^[a-z]{2}-[a-z]+-\\d$", var.AWS_REGION))
    error_message = "The AWS_REGION must be a valid region code (e.g., 'eu-central-1')."
  }
}

variable "env" {
  description = "The environment name (e.g., dev, prod) for tagging and configuration"
  type        = string
  default     = "dev"
  validation {
    condition     = contains(["dev", "prod", "test"], var.env)
    error_message = "The env must be one of: dev, prod, test."
  }
}

variable "AWS_ACCESS_KEY_ID" {
  description = "The AWS Access Key ID for authentication"
  type        = string
  sensitive   = true
}

variable "AWS_SECRET_ACCESS_KEY" {
  description = "The AWS Secret Access Key for authentication"
  type        = string
  sensitive   = true
}

variable "enable_network_address_usage_metrics" {
  description = "Enable network address usage metrics for the VPC"
  type        = bool
  default     = false
}

variable "instance_type" {
  description = "The EC2 instance type (e.g., t2.micro for Free Tier)"
  type        = string
  default     = "t2.micro"
  validation {
    condition     = contains(["t2.micro", "t2.small", "t3.micro"], var.instance_type)
    error_message = "The instance_type must be one of: t2.micro, t2.small, t3.micro."
  }
}

variable "key_name" {
  description = "The name of the SSH key pair for EC2 access"
  type        = string
  default     = "smoking-ec2-key"
}

variable "ec2_public_key" {
  description = "The public SSH key for EC2 instance access"
  type        = string
  sensitive   = true
  validation {
    condition     = can(regex("^ssh-rsa AAAA[0-9A-Za-z+/]+[=]{0,3}$", var.ec2_public_key))
    error_message = "The ec2_public_key must be a valid SSH public key starting with 'ssh-rsa'."
  }
}