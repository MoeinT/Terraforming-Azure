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

resource "azurerm_key_vault_secret" "example" {
  for_each     = var.properties
  name         = each.key
  value        = each.value.value
  key_vault_id = each.value.key_vault_id
}