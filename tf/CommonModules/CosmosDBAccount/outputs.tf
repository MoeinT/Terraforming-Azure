output "names" {
  value = { for i, j in azurerm_cosmosdb_account.CosmosDBAccount : i => j.name }
}

output "endpoint" {
  value = { for i, j in azurerm_cosmosdb_account.CosmosDBAccount : i => j.endpoint }
}

output "primaryKey" {
  value = { for i, j in azurerm_cosmosdb_account.CosmosDBAccount : i => j.primary_key }
}