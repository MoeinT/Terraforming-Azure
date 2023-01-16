module "kv" {
  source = "../../../CommonModules/KeyVault"
  env    = var.env

  properties = {
    "kv-tfdb-${var.env}" = {
      "rg-name" = module.rg.rg-names["rg-dbrg-${var.env}"],
      "loc"     = module.rg.rg-locations["rg-dbrg-${var.env}"],
      "sku"     = "standard"
      "tags"    = { "TerraformDeveloper" = "Moein" }
    }
  }
}

module "kvpolicies" {
  source = "../../../CommonModules/KVAccessPolicy"

  properties = {
    "moein-${var.env}" = {
      "key_vault_id"       = module.kv.KVids["kv-tfdb-${var.env}"],
      "object_id"          = var.moeinobji,
      "KeyPermissions"     = ["Get", "List", "Create"],
      "SecretPermissions"  = ["Get", "List", "Set"],
      "StoragePermissions" = ["Get", "List"]
    },
    "sp-${var.env}" = {
      "key_vault_id"       = module.kv.KVids["kv-tfdb-${var.env}"],
      "object_id"          = var.spobjid,
      "KeyPermissions"     = ["Get", "List", "Create"],
      "SecretPermissions"  = ["Get", "List", "Set"],
      "StoragePermissions" = ["Get", "List"]
    }
  }
}