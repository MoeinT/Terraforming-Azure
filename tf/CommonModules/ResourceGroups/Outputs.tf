output "rg-names" {
  value = { for i, j in azurerm_resource_group.AllRGs : j.name => j.name }
}

output "rg-locations" {
  value = { for i, j in azurerm_resource_group.AllRGs : j.name => j.location }
}