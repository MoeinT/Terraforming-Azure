module "azure" {
  source = "./azure"
  env    = var.env
  /* spobjid              = var.spobjid
  moeinobji            = var.moeinobji
  clientsecret         = var.clientsecret
  clientid             = var.clientid
  db_access_token_dev  = var.db_access_token_dev
  db_access_token_test = var.db_access_token_test
  db_access_token_qa   = var.db_access_token_qa
  db_access_token_prod = var.db_access_token_prod */
}