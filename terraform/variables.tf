# /terraform/variables.tf

variable "region" {
  description = "AWS region"
  default     = "eu-central-1"  # Fráncfort, Alemania (ideal para Múnich)
}

variable "env" {
  description = "Environment name"
  default     = "dev"
}

variable "db_password" {
  description = "Password for the RDS database"
  type        = string
  sensitive   = true
}
