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

resource "azurerm_eventhub_namespace" "EventHubsNameSpace" {
  for_each            = var.properties
  name                = each.key
  location            = each.value.location
  resource_group_name = each.value.resource_group_name
  sku                 = each.value.sku
  capacity            = each.value.capacity
  tags                = contains(keys(each.value), "tags") ? merge(local.DefaultTags, each.value.tags) : local.DefaultTags
}