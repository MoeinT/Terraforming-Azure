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

resource "azurerm_data_factory" "AllDFs" {
  for_each               = var.propeties
  name                   = each.key
  location               = each.value.loc
  resource_group_name    = each.value.rgname
  public_network_enabled = each.value.PublicAccessEnabled
  tags                   = contains(keys(each.value), "tags") ? merge(local.DefaultTags, each.value.tags) : local.DefaultTags

  dynamic "identity" {
    for_each = contains(keys(each.value), "ManagedIdentity") ? each.value.ManagedIdentity == true ? [1] : [] : []
    content {
      type = "SystemAssigned"
    }
  }

  lifecycle {
    ignore_changes = [vsts_configuration, github_configuration, customer_managed_key_id]
  }
}