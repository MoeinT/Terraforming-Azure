output "ws-url" {
  value = { for i, j in azurerm_databricks_workspace.AllWorkspaces : j.name => j.workspace_url }
}

output "ws-ids" {
  value = { for i, j in azurerm_databricks_workspace.AllWorkspaces : j.name => j.id }
}