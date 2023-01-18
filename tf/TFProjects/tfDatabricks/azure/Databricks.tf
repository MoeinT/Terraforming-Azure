module "db-ws" {
  source = "../../../CommonModules/DatabricksWorkspace"
  env    = var.env

  propeties = {
    "db-ws-${var.env}" = {
      "rgname" : module.rg.rg-names["rg-dbrg-${var.env}"],
      "loc" : module.rg.rg-locations["rg-dbrg-${var.env}"],
      "PublicAccessEnabled" : true
    }
  }
}

module "dbclusters" {
  source = "../../../CommonModules/DatabricksClusters"

  authentification = {
    "workspaceurl" : module.db-ws.ws-url["db-ws-${var.env}"],
    "workspaceid" : module.db-ws.ws-ids["db-ws-${var.env}"]
    "clientid" : var.clientid,
    "clientsecret" : var.clientsecret,
    "tenantid" : data.azurerm_client_config.current.tenant_id
  }

  properties = {
    "dbcluster-01-${var.env}" = {
      "spark_version" : "11.1.x-scala2.12",
      "node_type_id" : "Standard_DS3_v2",
      "singlenode" : true,
      "spark_conf" : {}
      "autotermination" = 20
    }
  }
}