module "adfs" {
  source = "../../../CommonModules/ADF"
  propeties = {
    "adf-tfdb-${var.env}" = {
      "loc"                 = module.rg.rg-locations["rg-dbrg-${var.env}"],
      "rgname"              = module.rg.rg-names["rg-dbrg-${var.env}"],
      "PublicAccessEnabled" = false,
      "ManagedIdentity"     = true,
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