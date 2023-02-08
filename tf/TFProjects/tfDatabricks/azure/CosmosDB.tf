module "cosmosdbaccount" {
  source = "../../../CommonModules/CosmosDBAccount"
  env    = var.env

  properties = {
    "testcosmos-${var.env}" = {
      "location"            = module.rg.rg-locations["rg-dbrg-02-${var.env}"],
      "resource_group_name" = module.rg.rg-names["rg-dbrg-02-${var.env}"],
      "kind"                = "GlobalDocumentDB",
      "consistency_level"   = "Session",
      "capabilities"        = ["EnableAggregationPipeline"]
      "geo_location"        = local.cosmosdb_geolocation
    }
  }
}

module "cosmosSqlDB" {
  source = "../../../CommonModules/CosmosDBsqlDB"
  properties = {
    "Families-${var.env}" = {
      "resource_group_name" = module.rg.rg-names["rg-dbrg-02-${var.env}"],
      "account_name"        = module.cosmosdbaccount.names["testcosmos-${var.env}"]
    }
  }
}

module "cosmosSqlContainer" {
  source = "../../../CommonModules/CosmosDBsqlContainer"
  properties = {
    "Families-con-${var.env}" = {
      "resource_group_name" = module.rg.rg-names["rg-dbrg-02-${var.env}"],
      "account_name"        = module.cosmosdbaccount.names["testcosmos-${var.env}"],
      "database_name"       = module.cosmosSqlDB.names["Families-${var.env}"],
      "partition_key_path"  = "/address/zipCode"
    }
  }
}