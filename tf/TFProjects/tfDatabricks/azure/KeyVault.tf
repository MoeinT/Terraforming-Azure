# module "kv" {
#   source = "../../../CommonModules/KeyVault"
#   env    = var.env

#   properties = {
#     "tf-01-kv-${var.env}" = {
#       "rg-name" = module.rg.rg-names["tfdemo-rg-${var.env}"],
#       "loc"     = module.rg.rg-locations["tfdemo-rg-${var.env}"],
#       "sku"     = "standard"
#       "tags"    = { "TerraformDeveloper" = "Moein" }
#     }
#   }
# }

# module "kvpolicies" {
#   source = "../../../CommonModules/KVAccessPolicy"

#   properties = {
#     "moein-${var.env}" = {
#       "key_vault_id"       = module.kv.KVids["tf-01-kv-${var.env}"],
#       "object_id"          = var.moeinobji,
#       "KeyPermissions"     = ["Get", "List", "Create"],
#       "SecretPermissions"  = ["Get", "List", "Set"],
#       "StoragePermissions" = ["Get", "List"]
#     },
#     "sp-${var.env}" = {
#       "key_vault_id"       = module.kv.KVids["tf-01-kv-${var.env}"],
#       "object_id"          = var.spobjid,
#       "KeyPermissions"     = ["Get", "List", "Create"],
#       "SecretPermissions"  = ["Get", "List", "Set"],
#       "StoragePermissions" = ["Get", "List"]
#     },
#     "adf-${var.env}" = {
#       "key_vault_id"   = module.kv.KVids["tf-01-kv-${var.env}"],
#       "object_id"      = module.adfs.principal_id["adf-tfdemo-01-${var.env}"],
#       "KeyPermissions" = ["Get", "UnwrapKey", "WrapKey"]
#     }
#   }
# }