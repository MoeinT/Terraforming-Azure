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

data "azurerm_client_config" "current" {}


resource "azurerm_key_vault" "AllKV" {
  for_each                    = var.properties
  name                        = each.key
  location                    = each.value.loc
  resource_group_name         = each.value.rg-name
  enabled_for_disk_encryption = true
  purge_protection_enabled    = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7
  sku_name                    = each.value.sku
  tags                        = contains(keys(each.value), "tags") ? merge(local.DefaultTags, each.value.tags) : local.DefaultTags

  network_acls {
    bypass         = "AzureServices"
    default_action = each.value.default_action
  }
}