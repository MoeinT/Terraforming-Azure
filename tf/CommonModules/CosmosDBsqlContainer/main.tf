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

  dynamic "indexing_policy" {
    for_each = contains(keys(each.value), "indexing_policy") == true ? [1] : []
    content {
      indexing_mode = each.value.indexing_policy

      dynamic "included_path" {
        for_each = contains(keys(each.value), "included_path") == true ? [1] : []
        content {
          path = each.value.included_path
        }
      }

      dynamic "excluded_path" {
        for_each = contains(keys(each.value), "excluded_path") == true ? [1] : []
        content {
          path = each.value.excluded_path
        }
      }

    }

  }

  dynamic "unique_key" {
    for_each = contains(keys(each.value), "unique_key_path") == true ? [1] : []
    content {
      paths = each.value.unique_key_path
    }
  }
}