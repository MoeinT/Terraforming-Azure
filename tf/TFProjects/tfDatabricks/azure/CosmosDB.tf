module "cosmosdbaccount" {
  source = "../../../CommonModules/CosmosDBAccount"
  properties = {
    "testcosmos-${var.env}" = {
      "location"            = module.rg.rg-locations["rg-dbrg-${var.env}"],
      "resource_group_name" = module.rg.rg-names["rg-dbrg-${var.env}"],
      "kind"                = "GlobalDocumentDB",
      "consistency_level"   = "Session",
      "capabilities" = [
        {
          "name" = "EnableAggregationPipeline"
        }
      ]
    }
  }
}