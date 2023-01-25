output "clusterids" {
  value = { for i, j in databricks_cluster.db-culster : j.cluster_name => j.id }
}