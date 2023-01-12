provider "azurerm" {
  features {}
}

provider "azuredevops" {
  org_service_url       = var.authentication.AdoOrgUrl
  personal_access_token = var.authentication.AdoToken
}