output "connection_string" {
  value = { for i, j in azurerm_application_insights.AllAppInsights : j.name => j.connection_string }
}

output "instrumentation_key" {
  value = { for i, j in azurerm_application_insights.AllAppInsights : j.name => j.instrumentation_key }
}

output "app_id" {
  value = { for i, j in azurerm_application_insights.AllAppInsights : j.name => j.app_id }
}

output "id" {
  value = { for i, j in azurerm_application_insights.AllAppInsights : j.name => j.id }
}