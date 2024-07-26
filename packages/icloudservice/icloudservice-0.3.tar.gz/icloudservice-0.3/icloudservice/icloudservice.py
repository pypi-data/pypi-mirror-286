import platform
import importlib.metadata
from dataclasses import dataclass
from rich.console import Console
from icloudservice.src.provider.aws.aws_provider import AWSCloud
from icloudservice.src.provider.azure.azure_provider import  AzureCloud

# Get the Python version
python_version = platform.python_version()

@dataclass
class Service():
    console = Console()
    
    def info(self):
        try:
            version = importlib.metadata.version('icloudservice')
        except importlib.metadata.PackageNotFoundError:
            version = 'unknown'
        # Get class name
        service_name = 'Cloud integration services for AWS and AZURE'
        log_message = (
        f"[yellow]Version library:[/yellow] [cyan]{version}[/cyan] \n"
        f"[yellow]Name:[/yellow] [cyan]icloudservice[/cyan] \n"
        f"[yellow]Description:[/yellow] [cyan]{service_name}[/cyan] \n"
        f"[yellow]Python Version:[/yellow] [cyan]{python_version}[/cyan] \n"
        )
        self.console.print(log_message)

@dataclass
class Provider():
    console = Console()

    def AWS(self,access_key:str,secret_key:str):
        self.console.print(f"[cyan]Aws[/cyan]")
        return AWSCloud(access_key,secret_key)
    
    def AZURE(self,subscription_id):
        return AzureCloud(subscription_id)