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

resource "azuredevops_serviceendpoint_azurerm" "AllEndPoins" {
  for_each              = var.properties
  service_endpoint_name = each.key
  project_id            = each.value.projectid
  description           = each.value.description

  credentials {
    serviceprincipalid  = each.value.clientid
    serviceprincipalkey = each.value.clientsecret
  }
  azurerm_spn_tenantid      = data.azurerm_client_config.current.tenant_id
  azurerm_subscription_id   = data.azurerm_client_config.current.subscription_id
  azurerm_subscription_name = data.azurerm_subscription.current.display_name
}

resource "azuredevops_resource_authorization" "AllAuth" {
  for_each = { for i, j in azuredevops_serviceendpoint_azurerm.AllEndPoins : j.project_id => j.id }

  project_id  = each.key
  resource_id = each.value
  authorized  = true
}