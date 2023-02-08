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

resource "azurerm_application_insights" "AllAppInsights" {
  for_each            = var.properties
  name                = each.key
  location            = each.value.location
  resource_group_name = each.value.resource_group_name
  workspace_id        = each.value.workspace_id
  application_type    = each.value.application_type
  retention_in_days   = each.value.retention_in_days
  tags                = contains(keys(each.value), "tags") ? merge(local.DefaultTags, each.value.tags) : local.DefaultTags
}

