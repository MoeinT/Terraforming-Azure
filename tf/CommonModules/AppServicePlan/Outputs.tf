output "app-ids" {
  value = { for i, j in azurerm_service_plan.AppServicePlan : j.name => j.id }
}