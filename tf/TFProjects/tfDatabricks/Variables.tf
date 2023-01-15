variable "env" {
  description = "Environment for resources"
  type        = string
  validation {
    condition     = contains(["dev", "test", "qa", "prod"], var.env)
    error_message = "Environment should be either: dev, test, qa or prod."
  }
}

# variable "spobjid" {
#   type      = string
#   sensitive = true
# }

# variable "moeinobji" {
#   type      = string
#   sensitive = true
# }

variable "clientsecret" {
  type      = string
  sensitive = true
}

variable "clientid" {
  type      = string
  sensitive = true
}