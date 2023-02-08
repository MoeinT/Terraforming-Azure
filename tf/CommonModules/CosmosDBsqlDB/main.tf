terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_cosmosdb_sql_database" "sqldbs" {
  for_each            = var.properties
  name                = each.key
  resource_group_name = each.value.resource_group_name
  account_name        = each.value.account_name
  throughput          = lookup(each.value, "throughput", null)
}