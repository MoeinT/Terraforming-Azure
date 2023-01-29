output "ns-names" {
  value = { for i, j in azurerm_eventhub_namespace.EventHubsNameSpace : j.name => j.name }
}

output "ns-connstr" {
  value = { for i, j in azurerm_eventhub_namespace.EventHubsNameSpace : j.name => j.default_primary_connection_string }
}