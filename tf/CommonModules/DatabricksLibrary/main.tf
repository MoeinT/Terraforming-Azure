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

provider "databricks" {
  host                        = var.authentification.workspaceurl
  azure_workspace_resource_id = var.authentification.workspaceid
  azure_client_id             = var.authentification.clientid
  azure_client_secret         = var.authentification.clientsecret
  azure_tenant_id             = var.authentification.tenantid
}

resource "databricks_library" "maven-EventHub" {
  for_each   = var.properties
  cluster_id = each.value.cluster_id

  dynamic "maven" {
    for_each = each.value.coordinates
    content {
      coordinates = maven.value.coordinates
    }
  }
}