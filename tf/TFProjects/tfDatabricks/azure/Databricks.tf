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

# module "dbclusters" {
#   source = "../../../CommonModules/DatabricksClusters"

#   authentification = {
#     "workspaceurl" : module.db-ws.ws-url["db-ws-tfdemo-01-${var.env}"],
#     "workspaceid" : module.db-ws.ws-ids["db-ws-tfdemo-01-${var.env}"]
#     "clientid" : var.clientid,
#     "clientsecret" : var.clientsecret,
#     "tenantid" : data.azurerm_client_config.current.tenant_id
#   }

#   properties = {
#     "cluster-01-${var.env}" = {
#       "clustername" : "dbcluster-01-${var.env}",
#       "sparkvs" : "11.1.x-scala2.12",
#       "sparknode" : "Standard_DS3_v2",
#       "minworkders" : 1,
#       "maxworkers" : 2,
#       "autotermination" = 20
#     }
#   }
# }