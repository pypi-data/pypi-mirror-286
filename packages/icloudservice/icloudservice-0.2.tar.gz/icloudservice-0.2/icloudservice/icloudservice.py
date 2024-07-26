import platform
import importlib.metadata
from dataclasses import dataclass
from rich.console import Console
from rich.logging import RichHandler

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