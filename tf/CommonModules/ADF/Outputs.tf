output "ids" {
  value = { for i, j in azurerm_data_factory.AllDFs : j.name => j.id }
}

output "principal_id" {
  value = { for i, j in azurerm_data_factory.AllDFs : j.name => j.identity.0.principal_id if length(j.identity) != 0 }
}
