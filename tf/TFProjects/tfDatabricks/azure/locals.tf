locals {
  backendtags = {
    "Environment_Type"  = "Backend"
    "InfoSeC"           = "Confidential"
    "Technical_Contact" = "moin.torabi@gmail.com"
  }

  db-authentification = {
    "workspaceurl" : module.db-ws.ws-url["db-ws-${var.env}"],
    "workspaceid" : module.db-ws.ws-ids["db-ws-${var.env}"]
    "clientid" : var.clientid,
    "clientsecret" : var.clientsecret,
    "tenantid" : data.azurerm_client_config.current.tenant_id
  }
}


