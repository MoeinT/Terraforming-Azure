output "ns-names" {
  value = { for i, j in azurerm_eventhub_namespace.EventHubsNameSpace : j.name => j.name }
}