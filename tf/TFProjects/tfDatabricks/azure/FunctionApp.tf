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

module "function-app" {
  source = "../../../CommonModules/FunctionApp"
  env    = var.env

  properties = {
    "functionapp-tfdb-${var.env}" = {
      "location"                    = module.rg.rg-locations["rg-dbrg-${var.env}"],
      "resource_group_name"         = module.rg.rg-names["rg-dbrg-${var.env}"],
      "storage_account_name"        = module.Sa.sa-names["sadb01${var.env}"],
      "storage_account_access_key"  = module.Sa.sa-accesskey["sadb01${var.env}"],
      "service_plan_id"             = module.app-service.app-ids["app-service-${var.env}"],
      "functions_extension_version" = "~4",
      "ManagedIdentity"             = true,
      "dotnet_version"              = "v6.0",
      "os_type"                     = "Windows",
      "sku_name"                    = "Y1"
    }
  }
}