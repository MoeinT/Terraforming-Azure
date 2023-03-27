
locals {
  backendtags = {
    "Environment_Type"  = "Backend"
    "InfoSeC"           = "Confidential"
    "Technical_Contact" = "moin.torabi@gmail.com"
  }

  /* db-authentification = {
    "workspaceurl" : module.db-ws.ws-url["db-ws-${var.env}"],
    "workspaceid" : module.db-ws.ws-ids["db-ws-${var.env}"]
    "clientid" : var.clientid,
    "clientsecret" : var.clientsecret,
    "tenantid" : data.azurerm_client_config.current.tenant_id
  }

  cosmosdb_geolocation = [
    {
      "location"          = "East Us",
      "failover_priority" = 0
    }
  ]

  adf_global_parameters = [
    {
      "name"  = "databricksurl"
      "type"  = "String",
      "value" = "https://${module.db-ws.ws-url["db-ws-${var.env}"]}"
    },
    {
      "name"  = "databrickscluster_id"
      "type"  = "String",
      "value" = module.dbclusters.clusterids["dbcluster-01-${var.env}"]
    },
    {
      "name" : "NotebookBasePath",
      "type" : "String",
      "value" : "/Repos/Dev/Terraforming-Azure/Databricks/TaxiTripETL"
    }
  ] */
}


