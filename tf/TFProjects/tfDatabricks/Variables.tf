variable "env" {
  description = "Environment for resources"
  type        = string
  validation {
    condition     = contains(["staging", "dev", "test", "qa"], var.env)
    error_message = "Environment should be either: staging, dev, test or qa."
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

# variable "clientsecret" {
#   type      = string
#   sensitive = true
# }

# variable "clientid" {
#   type      = string
#   sensitive = true
# }
