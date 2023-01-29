output "eventhubs-names" {
  value = { for i, j in azurerm_eventhub.AllEventHubs : j.name => j.name }
}