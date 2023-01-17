locals {
  single_node_config = {
    "spark.databricks.cluster.profile" : "singleNode"
    "spark.master" : "local[*]"
  }

  single_node_custom_tags = {
    "ResourceClass" = "SingleNode"
  }
}