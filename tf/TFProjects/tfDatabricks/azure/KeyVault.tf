
/* module "kv" {
  source = "../../../CommonModules/KeyVault"
  env    = var.env

  properties = {
    "kv-tfdb-${var.env}" = {
      "rg-name"        = module.rg.rg-names["rg-dbrg-${var.env}"],
      "loc"            = module.rg.rg-locations["rg-dbrg-${var.env}"],
      "default_action" = "Allow",
      "sku"            = "standard",
      "tags"           = { "TerraformDeveloper" = "Moein" }
    }
  }
} */

/* module "kvpolicies" {
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
      "SecretPermissions"  = ["Get", "List", "Set", "Delete", "Recover", "Restore"],
      "StoragePermissions" = ["Get", "List"]
    },
    "adf-${var.env}" = {
      "key_vault_id"      = module.kv.KVids["kv-tfdb-${var.env}"],
      "object_id"         = module.adfs.principal_id["adf-tfdb-${var.env}"],
      "KeyPermissions"    = ["Get", "UnwrapKey", "WrapKey", "List"],
      "SecretPermissions" = ["Get", "List"]
    }
  }
} */

/* module "kvsecrets" {
  source = "../../../CommonModules/KVSecrets"
  properties = {
    "client-id"           = { "value" = var.clientid, "key_vault_id" = module.kv.KVids["kv-tfdb-${var.env}"] },
    "client-secret"       = { "value" = var.clientsecret, "key_vault_id" = module.kv.KVids["kv-tfdb-${var.env}"] },
    "tenant-id"           = { "value" = data.azurerm_client_config.current.tenant_id, "key_vault_id" = module.kv.KVids["kv-tfdb-${var.env}"] },
    "sa-name"             = { "value" = module.Sa.sa-names["sadb01${var.env}"], "key_vault_id" = module.kv.KVids["kv-tfdb-${var.env}"] },
    "cosmosdb-endpoint"   = { "value" = module.cosmosdbaccount.endpoint["testcosmos-${var.env}"], "key_vault_id" = module.kv.KVids["kv-tfdb-${var.env}"] },
    "cosmosdb-primaryKey" = { "value" = module.cosmosdbaccount.primaryKey["testcosmos-${var.env}"], "key_vault_id" = module.kv.KVids["kv-tfdb-${var.env}"] },
    "db-access-token"     = { "value" = var.env == "dev" ? var.db_access_token_dev : var.env == "test" ? var.db_access_token_test : var.env == "qa" ? var.db_access_token_qa : var.db_access_token_prod, "key_vault_id" = module.kv.KVids["kv-tfdb-${var.env}"] }
  }
} */