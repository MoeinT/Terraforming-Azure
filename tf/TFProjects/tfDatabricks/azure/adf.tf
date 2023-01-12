# module "adfs" {
#   source = "../../../CommonModules/ADF"
#   propeties = {
#     "adf-tfdemo-01-${var.env}" = {
#       "loc"                 = module.rg.rg-locations["tfdemo-rg-${var.env}"],
#       "rgname"              = module.rg.rg-names["tfdemo-rg-${var.env}"],
#       "PublicAccessEnabled" = false,
#       "ManagedIdentity"     = true,
#       "tags"                = { "TerraformDeveloper" = "Moein" }
#     }
#   }
# }