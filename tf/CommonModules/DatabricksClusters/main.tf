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
  spark_version = each.value.spark_version
  node_type_id  = each.value.node_type_id

  autotermination_minutes = each.value.autotermination

  dynamic "autoscale" {
    for_each = contains(keys(each.value), "minworkders") && contains(keys(each.value), "maxworkers") ? [1] : []
    content {
      min_workers = each.value.minworkders
      max_workers = each.value.maxworkers
    }
  }

  spark_conf = contains(keys(each.value), "singlenode") ? each.value.singlenode == true ? {
    "spark.databricks.cluster.profile" : "singleNode"
    "spark.master" : "local[*]"
  } : null : null

  custom_tags = contains(keys(each.value), "singlenode") ? each.value.singlenode == true ? {
    "ResourceClass" = "SingleNode"
  } : null : null

}