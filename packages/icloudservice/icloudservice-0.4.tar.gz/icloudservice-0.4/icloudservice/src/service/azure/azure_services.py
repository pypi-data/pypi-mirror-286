from azure.storage.blob import BlobServiceClient
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient
from rich.progress import Progress


class AzureService:

    def __init__(self, subscription_id: str, credential: DefaultAzureCredential = None):
        self.subscription_id = subscription_id
        self.credential = credential or DefaultAzureCredential()
        
        # Configura los endpoints para los servicios específicos
        self.blob_endpoint = f"https://{subscription_id}.blob.core.windows.net"
        self.cosmos_endpoint = f"https://{subscription_id}.documents.azure.com:443/"
        self.service_bus_endpoint = f"https://{subscription_id}.servicebus.windows.net/"

    def create_blob_client(self):
        if self.blob_endpoint:
            return BlobServiceClient(account_url=self.blob_endpoint, credential=self.credential)
        else:
            raise ValueError("Blob endpoint is not configured")

    def create_cosmos_client(self):
        if self.cosmos_endpoint:
            return CosmosClient(endpoint=self.cosmos_endpoint, credential=self.credential)
        else:
            raise ValueError("Cosmos endpoint is not configured")
    def create_service_bus_client(self):
        if self.service_bus_endpoint:
            return ServiceBusClient(fully_qualified_namespace=self.service_bus_endpoint, credential=self.credential)
        else:
            raise ValueError("Service Bus endpoint is not configured")

class BlobStorageService:
    def __init__(self, azure_service: AzureService, container_name: str):
        self.client = azure_service.create_blob_client()
        self.container_name = container_name

    def upload(self, local_path: str, blob_name: str):
        blob_client = self.client.get_blob_client(container=self.container_name, blob=blob_name)
        with open(local_path, "rb") as data:
            blob_client.upload_blob(data)

    def download(self, blob_name: str, local_path: str):
        blob_client = self.client.get_blob_client(container=self.container_name, blob=blob_name)
        with open(local_path, "wb") as data:
            data.write(blob_client.download_blob().readall())

    def list_blobs(self):
        container_client = self.client.get_container_client(self.container_name)
        blobs = list(container_client.list_blobs())
        total_blobs = len(blobs)
        with Progress() as progress:
            task = progress.add_task("[cyan]Listing blobs...", total=total_blobs)
            blob_names = []
            for blob in blobs:
                blob_names.append(blob.name)
                progress.update(task, advance=1)

        return blob_names

class CosmosDBService:
    def __init__(self, azure_service: AzureService, database_name: str):
        self.client = azure_service.create_cosmos_client()
        self.database = self.client.get_database_client(database_name)

    def create_container(self, container_name: str):
        self.database.create_container(id=container_name)

    def query_items(self, container_name: str, query: str):
        container = self.database.get_container_client(container_name)
        return list(container.query_items(query=query, enable_cross_partition_query=True))

class ServiceBusService:
    def __init__(self, azure_service: AzureService):
        self.client = azure_service.create_service_bus_client()

    def send_message(self, queue_name: str, message_body: str):
        sender = self.client.get_queue_sender(queue_name)
        with sender:
            message = ServiceBusMessage(message_body)
            sender.send_messages(message)

    def receive_messages(self, queue_name: str):
        receiver = self.client.get_queue_receiver(queue_name)
        with receiver:
            messages = receiver.receive_messages()
            return [msg.body for msg in messages]