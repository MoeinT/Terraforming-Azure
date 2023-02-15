variable "env" {
  type = string
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

variable "listOfMavenPackages" {
  type    = list(string)
  default = ["com.microsoft.azure:azure-eventhubs-spark_2.12:2.3.22", "com.azure.cosmos.spark:azure-cosmos-spark_3-3_2-12:4.15.0"]
}
