output "names" {
  value = { for i, j in azurerm_cosmosdb_sql_database.sqldbs : i => j.name }
}