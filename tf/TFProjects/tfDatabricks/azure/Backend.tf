
/* resource "azurerm_resource_group" "RGBackend" {
  name     = "tfstate-rg"
  location = "West Europe"
  tags     = merge(local.backendtags, { "Terraform_Developer" : "Moein" })
} */

/* resource "azurerm_storage_account" "SABackend" {
  name                            = "tfstatesademo01"
  resource_group_name             = azurerm_resource_group.RGBackend.name
  location                        = azurerm_resource_group.RGBackend.location
  account_tier                    = "Standard"
  is_hns_enabled                  = true
  account_replication_type        = "LRS"
  allow_nested_items_to_be_public = true
  tags                            = merge(local.backendtags, { "Terraform_Developer" : "Moein" })

  network_rules {
    default_action = "Allow"
    bypass         = ["AzureServices"]
  }

} */

/* resource "azurerm_storage_data_lake_gen2_filesystem" "ConBackend" {
  name               = "tfstate-container"
  storage_account_id = azurerm_storage_account.SABackend.id
} */