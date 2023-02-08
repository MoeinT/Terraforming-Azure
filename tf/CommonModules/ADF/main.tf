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
    for_each = lookup(each.value, "ManagedIdentity", false) == true ? [1] : []
    content {
      type = "SystemAssigned"
    }
  }

  dynamic "global_parameter" {
    for_each = contains(keys(each.value), "global_parameter") ? each.value.global_parameter : []
    content {
      name  = global_parameter.value.name
      type  = global_parameter.value.type
      value = global_parameter.value.value
    }
  }

  lifecycle {
    ignore_changes = [vsts_configuration, github_configuration, customer_managed_key_id]
  }
}