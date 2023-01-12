output "ids" {
  value = { for i, j in azurerm_log_analytics_workspace.AllLogs : j.name => j.id }
}