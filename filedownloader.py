# Azure Imports For Blob Storage
from azure.storage.blob.baseblobservice import BaseBlobService
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
import os

#name of your storage account and the access key from Settings->AccessKeys->key1
name ='replace'
key = 'replace'
blob_service=BaseBlobService(account_name=name, account_key=key)
block_blob_service = BlockBlobService(account_name=name, account_key=key)
#name of the container
# # Get All Containers
containers = blob_service.list_containers()
container_name = ""
for c in containers:
    # Save Contianer name if it matches images
    if c.name == 'images':
        container_name = c.name

# Get All Blobs in Container
generator = block_blob_service.list_blobs(container_name)

#code below lists all the blobs in the container and downloads them one after another
for blob in generator:
    print(blob.name)
    print("{}".format(blob.name))
    #check if the path contains a folder structure, create the folder structure
    if "/" in "{}".format(blob.name):
        #extract the folder path and check if that folder exists locally, and if not create it
        head, tail = os.path.split("{}".format(blob.name))
        if (os.path.isdir(os.getcwd()+ "/" + head)):
            #download the files to this directory
            block_blob_service.get_blob_to_path(container_name,blob.name,os.getcwd()+ "/" + head + "/" + tail)
            print("Copied File To Dir: " + blob.name)
        else:
            #create the diretcory and download the file to it
            print("directory doesn't exist, creating it now")
            os.makedirs(os.getcwd()+ "/" + head, exist_ok=True)
            print("directory created, download initiated")
            block_blob_service.get_blob_to_path(container_name,blob.name,os.getcwd()+ "/" + head + "/" + tail)
    else:
        block_blob_service.get_blob_to_path(container_name,blob.name,blob.name)
