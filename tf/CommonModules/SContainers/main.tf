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

resource "azurerm_storage_data_lake_gen2_filesystem" "AllContainers" {
  for_each           = var.properties
  name               = each.key
  storage_account_id = each.value.storage_account_id
}