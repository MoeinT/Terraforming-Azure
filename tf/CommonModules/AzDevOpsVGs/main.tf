terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0.0"
    }

    azuredevops = {
      source  = "microsoft/azuredevops"
      version = ">= 0.2.2"
    }
  }
}

provider "azurerm" {
  features {}
}

provider "azuredevops" {
  org_service_url       = var.authentication.AdoOrgUrl
  personal_access_token = var.authentication.AdoToken
}

resource "azuredevops_variable_group" "AllVgs" {

  for_each     = var.properties
  name         = each.key
  project_id   = each.value.projectid
  description  = each.value.description
  allow_access = false

  dynamic "key_vault" {
    for_each = contains(keys(each.value), "service_endpoint_id") && contains(keys(each.value), "kvname") ? [1] : []
    content {
      name                = each.value.kvname
      service_endpoint_id = each.value.endpointid
    }
  }

  dynamic "variable" {
    for_each = each.value.variables
    content {
      name = variable.value.name
    }
  }
}