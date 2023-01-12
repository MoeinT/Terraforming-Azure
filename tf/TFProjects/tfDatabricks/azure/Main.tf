terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0.0"
    }

    databricks = {
      source = "databricks/databricks"
    }
  }
}

data "azurerm_client_config" "current" {
}

data "azurerm_subscription" "current" {

}

provider "azurerm" {
  features {}
}