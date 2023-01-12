output "KVids" {
  value = { for i, j in azurerm_key_vault.AllKV : i => j.id }
}

output "KVnames" {
  value = { for i, j in azurerm_key_vault.AllKV : i => j.name }
}