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
  source           = "../../../CommonModules/DatabricksClusters"
  authentification = local.db-authentification

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

module "dblibraries" {
  source           = "../../../CommonModules/DatabricksLibrary"
  authentification = local.db-authentification

  properties = {
    module.dbclusters.clusterids["dbcluster-01-${var.env}"] : ["com.microsoft.azure:azure-eventhubs-spark_2.12:2.3.22", "com.databricks.training:databricks-cosmosdb-spark2.2.0-scala2.11:1.0.0"]
  }
}