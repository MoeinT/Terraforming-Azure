module "cosmosdbaccount" {
  source = "../../../CommonModules/CosmosDBAccount"
  env    = var.env

  properties = {
    "testcosmos-${var.env}" = {
      "location"            = module.rg.rg-locations["rg-dbrg-${var.env}"],
      "resource_group_name" = module.rg.rg-names["rg-dbrg-${var.env}"],
      "kind"                = "GlobalDocumentDB",
      "consistency_level"   = "Session",
      "capabilities"        = ["EnableAggregationPipeline"]
      "geo_location"        = local.cosmosdb_geolocation
    }
  }
}