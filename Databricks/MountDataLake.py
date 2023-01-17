# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *
import typing

# COMMAND ----------

class MountSP:
    
    def __init__(self, allcontainers: typing.List[str], client_id: str, client_secret: str, tenant_id: str, storageaccount: str) -> None:
        self.allcontainers = allcontainers
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.storageaccount = storageaccount
    
    @property
    def GetConfig(self) -> dict:
        
        return (
            {
                "fs.azure.account.auth.type": "OAuth",
                "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
                "fs.azure.account.oauth2.client.id": self.client_id,
                "fs.azure.account.oauth2.client.secret": self.client_secret,
                "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/token"
            }
        )
    
    def MountStorageAccount(self) -> None:
        
        for container in self.allcontainers:
            mount_point = f"/mnt/{self.storageaccount}/{container}"
            if mount_point in [mnt.mountPoint for mnt in dbutils.fs.mounts()]:
                print(f"Directory '{mount_point}' is already mounted!")
                continue
            else:
                print(f"Mounting {mount_point}...")
                dbutils.fs.mount(
                    source = f"abfss://{container}@{self.storageaccount}.dfs.core.windows.net/",
                    mount_point = mount_point,
                    extra_configs = self.GetConfig
                )
        

# COMMAND ----------

MountObject = MountSP(
    allcontainers  = ["data"], 
    client_id      = dbutils.secrets.get(scope = "key-vault-sctlh", key = "client-id"),
    client_secret  = dbutils.secrets.get(scope = "key-vault-sctlh", key = "client-secret"),
    tenant_id      = dbutils.secrets.get(scope = "key-vault-sctlh", key = "tenant-id"),
    storageaccount = dbutils.secrets.get(scope = "key-vault-sctlh", key = "sa-name")
)

MountObject.MountStorageAccount()

# COMMAND ----------

dbutils.fs.mounts()
