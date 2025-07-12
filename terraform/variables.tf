# # /terraform/variables.tf
# 
# variable "region" {
#   description = "AWS region"
#   default     = "eu-central-1"  # Fráncfort, Alemania (ideal para Múnich)
# }
# 
# variable "env" {
#   description = "Environment name"
#   default     = "dev"
# }
# 
# variable "db_password" {
#   description = "Password for the RDS database"
#   type        = string
#   sensitive   = true
# }

# /terraform/variables.tf

# /workspaces/Body_Signals_of_Smoking---AWS-Terraform-testing/terraform/variables.tf
variable "AWS_REGION" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
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

variable "enable_network_address_usage_metrics" {
  description = "Enable network address usage metrics for the VPC"
  type        = bool
  default     = false  # Desactivado por defecto para evitar errores
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  description = "SSH key name"
  type        = string
  default     = "smoking-ec2-key"
}