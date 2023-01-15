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

resource "azurerm_storage_account" "AllSa" {
  for_each = var.properties

  name                            = each.key
  resource_group_name             = each.value.rgname
  location                        = each.value.loc
  account_tier                    = each.value.account_tier
  is_hns_enabled                  = true
  account_replication_type        = "LRS"
  allow_nested_items_to_be_public = each.value.allow_nested_items_to_be_public
  tags                            = contains(keys(each.value), "tags") ? merge(local.DefaultTags, each.value.tags) : local.DefaultTags

  network_rules {
    default_action = each.value.default_action
    bypass         = ["AzureServices"]
  }

}