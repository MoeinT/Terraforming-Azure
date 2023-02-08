output "names" {
  value = { for i, j in azurerm_cosmosdb_account.CosmosDBAccount : i => j.name }
}