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
  for_each      = var.properties
  cluster_name  = each.value.clustername
  spark_version = each.value.sparkvs
  node_type_id  = each.value.sparknode

  autotermination_minutes = each.value.autotermination
  autoscale {
    min_workers = each.value.minworkders
    max_workers = each.value.maxworkers
  }
}