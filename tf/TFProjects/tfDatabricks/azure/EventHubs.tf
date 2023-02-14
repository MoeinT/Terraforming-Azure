
/* module "eventhubs-ns" {
  source = "../../../CommonModules/EventHubsNameSpace"
  properties = {
    "eventhubns-tfdb-${var.env}" = {
      "location"            = module.rg.rg-locations["rg-dbrg-${var.env}"],
      "resource_group_name" = module.rg.rg-names["rg-dbrg-${var.env}"],
      "sku"                 = "Standard",
      "capacity"            = 1,
      "tags"                = { "TerraformDeveloper" = "Moein" }
    }
  }
  env = var.env
} */

/* module "EventHubs" {
  source = "../../../CommonModules/EventHubs"
  properties = {
    "streamtweets-tfdb-${var.env}" = {
      "namespace_name"      = module.eventhubs-ns.ns-names["eventhubns-tfdb-${var.env}"],
      "resource_group_name" = module.rg.rg-names["rg-dbrg-${var.env}"],
      "partition_count"     = 1,
      "message_retention"   = 1
    }
  }
  env = var.env
} */