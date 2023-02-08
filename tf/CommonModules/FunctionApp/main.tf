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

resource "azurerm_windows_function_app" "TestFunctionApp" {
  for_each = var.properties

  name                        = each.key
  location                    = each.value.location
  resource_group_name         = each.value.resource_group_name
  service_plan_id             = each.value.service_plan_id
  storage_account_name        = each.value.storage_account_name
  storage_account_access_key  = each.value.storage_account_access_key
  functions_extension_version = each.value.functions_extension_version
  client_certificate_mode     = "Optional"
  https_only                  = "true"
  tags                        = contains(keys(each.value), "tags") ? merge(local.DefaultTags, each.value.tags) : local.DefaultTags

  dynamic "identity" {
    for_each = lookup(each.value, "ManagedIdentity", false) == true ? [1] : []
    content {
      type = "SystemAssigned"
    }
  }

  site_config {
    always_on = false
    application_stack {
      dotnet_version = each.value.dotnet_version
    }
  }

}