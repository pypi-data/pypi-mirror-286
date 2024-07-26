from azure.identity import DefaultAzureCredential
from icloudservice.src.service.azure.azure_services import AzureService
from icloudservice.src.service.azure.azure_services import BlobStorageService, CosmosDBService, ServiceBusService


class AzureCloud(AzureService):
    def __init__(self, subscription_id: str, credential: DefaultAzureCredential = None):
        self.subscription_id = subscription_id
        self.credential = credential or DefaultAzureCredential()
        super().__init__(subscription_id=subscription_id)

    def BlobStorageService(self, container_name: str):
        return BlobStorageService(self, container_name)

    def CosmosDBService(self, database_name: str):
        return CosmosDBService(self, database_name)

    def ServiceBusService(self):
        return ServiceBusService(self)