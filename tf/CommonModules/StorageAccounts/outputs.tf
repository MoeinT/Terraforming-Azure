output "sa-names" {
  value = { for i, j in azurerm_storage_account.AllSa : i => j.name }
}

output "ids" {
  value = { for i, j in azurerm_storage_account.AllSa : i => j.id }
}

output "sa-accesskey" {
  value = { for i, j in azurerm_storage_account.AllSa : i => j.primary_access_key }
}