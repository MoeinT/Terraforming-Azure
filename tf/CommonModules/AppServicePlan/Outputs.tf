output "app-ids" {
  value = { for i, j in azurerm_app_service_plan.AppServicePlan : j.name => j.id }
}