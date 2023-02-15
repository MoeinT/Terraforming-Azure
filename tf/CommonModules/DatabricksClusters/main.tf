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

provider "azurerm" {
  features {}
}

#Authenticating with Azure Service Principal
provider "databricks" {
  host                        = var.authentification.workspaceurl
  azure_workspace_resource_id = var.authentification.workspaceid
  azure_client_id             = var.authentification.clientid
  azure_client_secret         = var.authentification.clientsecret
  azure_tenant_id             = var.authentification.tenantid
}

resource "databricks_cluster" "db-culster" {
  for_each                = var.properties
  cluster_name            = each.key
  spark_version           = each.value.spark_version
  node_type_id            = each.value.node_type_id
  autotermination_minutes = each.value.autotermination
  num_workers             = contains(keys(each.value), "singlenode") ? each.value.singlenode ? null : contains(keys(each.value), "min_workers") && contains(keys(each.value), "max_workers") ? null : each.value.num_workers : contains(keys(each.value), "min_workers") && contains(keys(each.value), "max_workers") ? null : each.value.num_workers
  spark_conf              = contains(keys(each.value), "singlenode") ? each.value.singlenode ? contains(keys(each.value), "spark_conf") ? merge(local.single_node_config, each.value.spark_conf) : local.single_node_config : contains(keys(each.value), "spark_conf") ? each.value.spark_conf : null : contains(keys(each.value), "spark_conf") ? each.value.spark_conf : null
  custom_tags             = contains(keys(each.value), "singlenode") ? each.value.singlenode ? local.single_node_custom_tags : null : null

  dynamic "autoscale" {
    for_each = contains(keys(each.value), "min_workers") && contains(keys(each.value), "max_workers") ? [1] : []
    content {
      min_workers = each.value.min_workers
      max_workers = each.value.max_workers
    }
  }

  dynamic "library" {
    for_each = contains(keys(each.value), "ListOfLibraries") ? each.value.ListOfLibraries : []
    content {
      maven {
        coordinates = library.value
      }
    }
  }
}