
/* resource "azurerm_function_app" "example" {
  name                       = "test-azure-functions"
  location                   = azurerm_resource_group.example.location
  resource_group_name        = azurerm_resource_group.example.name
  app_service_plan_id        = azurerm_app_service_plan.example.id
  storage_account_name       = azurerm_storage_account.example.name
  storage_account_access_key = azurerm_storage_account.example.primary_access_key
} */

module "app-service" {
  source = "../../../CommonModules/AppServicePlan"
  properties = {
    "app-service-${var.env}" = {
      "location"            = module.rg.rg-locations["rg-dbrg-${var.env}"],
      "resource_group_name" = module.rg.rg-names["rg-dbrg-${var.env}"],
      "os_type"             = "Windows",
      "sku_name"            = "Y1"
    }
  }
}