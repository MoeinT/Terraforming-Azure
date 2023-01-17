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

  backend "azurerm" {
    resource_group_name  = "tfstate-rg"
    storage_account_name = "tfstatesademo01"
    container_name       = "tfstate-container"
  }
}

provider "azurerm" {
  features {}
}

output "test" {
  value = module.azure.test-sa
}