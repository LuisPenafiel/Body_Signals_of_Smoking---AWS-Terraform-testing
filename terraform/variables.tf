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

variable "AWS_REGION" {
  description = "AWS region"
  type        = string
}

variable "env" {
  description = "Environment name (e.g., dev, prod)"
  type        = string
  default     = "dev"  # Opcional: un valor por defecto
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