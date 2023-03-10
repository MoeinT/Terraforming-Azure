module "adfs" {
  source = "../../../CommonModules/ADF"
  propeties = {
    "adf-tfdb-${var.env}" = {
      "loc"                 = module.rg.rg-locations["rg-dbrg-${var.env}"],
      "rgname"              = module.rg.rg-names["rg-dbrg-${var.env}"],
      "PublicAccessEnabled" = false,
      "ManagedIdentity"     = true,
      "global_parameter"    = local.adf_global_parameters
      "tags"                = { "TerraformDeveloper" = "Moein" }
    }
  }
}

# Create a KeyVault Linked Service
resource "azurerm_data_factory_linked_service_key_vault" "ls-kv-adf" {
  name            = "ls-kv-${var.env}"
  data_factory_id = module.adfs.ids["adf-tfdb-${var.env}"]
  key_vault_id    = module.kv.KVids["kv-tfdb-${var.env}"]
}

# Create a linked service to Databricks
resource "azurerm_data_factory_linked_service_azure_databricks" "ls-db-adf" {
  name                = "ls-db-${var.env}"
  data_factory_id     = module.adfs.ids["adf-tfdb-${var.env}"]
  description         = "ADB Linked Service via Access Token"
  adb_domain          = "@linkedService().databricksurl"
  existing_cluster_id = "@linkedService().databrickscluster_id"

  parameters = {
    databrickscluster_id = ""
    databricksurl        = ""
  }

  key_vault_password {
    linked_service_name = azurerm_data_factory_linked_service_key_vault.ls-kv-adf.name
    secret_name         = "db-access-token"
  }
}

# Linked Service to DataLake Gen2
resource "azurerm_data_factory_linked_service_data_lake_storage_gen2" "ls-dl" {
  name                 = "ls-dl-${var.env}"
  data_factory_id      = module.adfs.ids["adf-tfdb-${var.env}"]
  url                  = "https://${module.Sa.sa-names["sadb01${var.env}"]}.dfs.core.windows.net"
  use_managed_identity = true
}