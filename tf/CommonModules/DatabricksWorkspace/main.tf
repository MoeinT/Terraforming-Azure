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

resource "azurerm_databricks_workspace" "AllWorkspaces" {
  for_each                      = var.propeties
  name                          = each.key
  resource_group_name           = each.value.rgname
  location                      = each.value.loc
  managed_resource_group_name   = "db-managed-rg-${var.env}"
  sku                           = "premium"
  public_network_access_enabled = each.value.PublicAccessEnabled
  tags                          = contains(keys(each.value), "tags") ? merge(local.DefaultTags, each.value.tags) : local.DefaultTags
}