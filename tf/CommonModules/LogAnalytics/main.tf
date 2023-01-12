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

resource "azurerm_log_analytics_workspace" "AllLogs" {
  for_each            = var.properties
  name                = each.key
  location            = each.value.loc
  resource_group_name = each.value.rgname
  sku                 = each.value.sku
  retention_in_days   = each.value.retention_in_days
  tags                = contains(keys(each.value), "tags") ? merge(local.DefaultTags, each.value.tags) : local.DefaultTags
}