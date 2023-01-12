output "EndpointIds" {
  value = { for i, j in azuredevops_serviceendpoint_azurerm.AllEndPoins : j.service_endpoint_name => j.id }
}