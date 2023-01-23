variable "env" {
  description = "Environment for resources"
  type        = string
  validation {
    condition     = contains(["dev", "test", "qa", "prod"], var.env)
    error_message = "Environment should be either: dev, test, qa or prod."
  }
}

variable "spobjid" {
  type      = string
  sensitive = true
}

variable "moeinobji" {
  type      = string
  sensitive = true
}

variable "clientsecret" {
  type      = string
  sensitive = true
}

variable "clientid" {
  type      = string
  sensitive = true
}

variable "db_access_token_dev" {
  type      = string
  sensitive = true
}

variable "db_access_token_test" {
  type      = string
  sensitive = true
}

variable "db_access_token_qa" {
  type      = string
  sensitive = true
}

variable "db_access_token_prod" {
  type      = string
  sensitive = true
}