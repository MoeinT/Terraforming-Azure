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

resource "azurerm_cosmosdb_account" "CosmosDBAccount" {

  for_each                        = var.properties
  name                            = each.key
  location                        = each.value.location
  resource_group_name             = each.value.resource_group_name
  kind                            = each.value.kind
  offer_type                      = lookup(each.value, "offer_type", "Standard")
  enable_automatic_failover       = lookup(each.value, "enable_automatic_failover", false)
  enable_free_tier                = lookup(each.value, "enable_free_tier", true)
  enable_multiple_write_locations = lookup(each.value, "enable_multiple_write_locations", false)

  consistency_policy {
    consistency_level       = each.value.consistency_level
    max_interval_in_seconds = lookup(each.value, "maxIntervalInSeconds", 5)
    max_staleness_prefix    = lookup(each.value, "maxStalenessPrefix", 100)
  }

  dynamic "capabilities" {
    for_each = each.value.capabilities
    content {
      name = capabilities.value.name
    }
  }

  dynamic "identity" {
    for_each = lookup(each.value, "ManagedIdentity", false) == true ? [1] : []
    content {
      type = "SystemAssigned"
    }
  }

  geo_location {
    location          = "eastus"
    failover_priority = 1
  }

  geo_location {
    location          = "westus"
    failover_priority = 0
  }
}