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

resource "azurerm_cosmosdb_sql_container" "CosmosContainers" {
  for_each              = var.properties
  name                  = each.key
  resource_group_name   = each.value.resource_group_name
  account_name          = each.value.account_name
  database_name         = each.value.database_name
  partition_key_path    = each.value.partition_key_path
  partition_key_version = lookup(each.value, "partition_key_version", 1)
  throughput            = lookup(each.value, "throughput", 400)

  indexing_policy {
    indexing_mode = lookup(each.value, "indexing_mode", null)

    included_path {
      path = lookup(each.value, "included_path", null)
    }

    excluded_path {
      path = lookup(each.value, "excluded_path", null)
    }
  }

  unique_key {
    paths = lookup(each.value, "unique_key", null)
  }
}