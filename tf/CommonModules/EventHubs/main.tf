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

resource "azurerm_eventhub" "AllEventHubs" {
  for_each            = var.properties
  name                = each.key
  namespace_name      = each.value.namespace_name
  resource_group_name = each.value.resource_group_name
  partition_count     = each.value.partition_count
  message_retention   = each.value.message_retention
}