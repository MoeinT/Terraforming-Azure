import configparser
import os

from azure.storage.blob import BlobServiceClient


def load_files_into_azure(local_path, connection_string, target_path):

    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )

        if os.path.exists(local_path):

            files = os.listdir(os.path.join(local_path))
            print("\nUploading the files to Azure dlgen2..")

            for file in files:

                blob_client = blob_service_client.get_blob_client(
                    container=target_path, blob=file
                )

                upload_file_path = os.path.join(local_path, file)
                blob_client.upload_blob(upload_file_path, overwrite=True)

            print("All files successfully uploaded.")
        else:
            print("Directory not found!")

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    config = configparser.ConfigParser(interpolation=None)
    config.read("config.ini")

    connection_string = config["Azure"]["connection_string"]
    target_path = config["Azure"]["target_path"]
    local_path = os.path.join("datasets")

    load_files_into_azure(
        local_path=local_path,
        connection_string=connection_string,
        target_path=target_path,
    )