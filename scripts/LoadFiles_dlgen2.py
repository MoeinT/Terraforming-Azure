import configparser
import typing
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import ClientSecretCredential

# Connect using a SP
def initialize_storage_account_ad(
    storage_account_name, client_id, client_secret, tenant_id
):

    try:
        global service_client

        credential = ClientSecretCredential(tenant_id, client_id, client_secret)

        service_client = DataLakeServiceClient(
            account_url="{}://{}.dfs.core.windows.net".format("https", storage_account_name),
            credential=credential,
        )

    except Exception as e:
        print(e)


# Create a container
def create_file_system(container_name):

    try:
        service_client.create_file_system(file_system=container_name)

    except Exception as e:
        print(e)


# Create a directory
def create_directories(container_name, directory_names: typing.List[str]):

    try:
        file_system_client = service_client.get_file_system_client(
            file_system=container_name
        )

        for directory in directory_names:
            file_system_client.create_directory(directory)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    config = configparser.ConfigParser(interpolation=None)
    config.read("config.ini")

    client_id = config["Azure"]["client_id"]
    client_secret = config["Azure"]["client_secret"]
    tenant_id = config["Azure"]["tenant_id"]

    initialize_storage_account_ad(
        storage_account_name="sadb01dev",
        client_id=client_id,
        client_secret=client_secret,
        tenant_id=tenant_id,
    )

    # create_file_system(container_name = "container-test")
    create_directories(
        container_name="commonfiles-dev", directory_names=["Raw", "Processed"]
    )
