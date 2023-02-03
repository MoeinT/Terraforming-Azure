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

resource "azurerm_app_service_plan" "AppServicePlan" {
  for_each            = var.properties
  name                = each.key
  location            = each.value.location
  resource_group_name = each.value.resource_group_name
  kind                = each.value.kind

  sku {
    tier = each.value.sku
    size = each.value.size
  }
}