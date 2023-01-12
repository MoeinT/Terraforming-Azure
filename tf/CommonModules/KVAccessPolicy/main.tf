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

resource "azurerm_key_vault_access_policy" "Policies" {
  for_each                = var.properties
  key_vault_id            = each.value.key_vault_id
  tenant_id               = data.azurerm_client_config.current.tenant_id
  object_id               = each.value.object_id
  key_permissions         = lookup(each.value, "KeyPermissions", [])
  secret_permissions      = lookup(each.value, "SecretPermissions", [])
  certificate_permissions = lookup(each.value, "CertificatePermissions", [])
  storage_permissions     = lookup(each.value, "StoragePermissions", [])
}