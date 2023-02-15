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
      /* "ListOfLibraries" = var.listOfMavenPackages */
    }
  }
}