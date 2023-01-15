# Resource Group
module "rg" {
  source = "../../../CommonModules/ResourceGroups"
  properties = {
    "rg-dbrg-${var.env}" = {
      "loc" : "East Us",
      "tags" : { "TerraformDeveloper" = "Moein" }
    }
  }
  env = var.env
}

# Storage Account
module "Sa" {
  source = "../../../CommonModules/StorageAccounts"
  properties = {
    "sadb01${var.env}" = {
      "rgname"                          = module.rg.rg-names["rg-dbrg-${var.env}"],
      "loc"                             = module.rg.rg-locations["rg-dbrg-${var.env}"],
      "account_tier"                    = "Standard"
      "allow_nested_items_to_be_public" = false
      "default_action"                  = "Allow"
      "tags"                            = { "TerraformDeveloper" = "Moein" }
    }
  }
  env = var.env
}