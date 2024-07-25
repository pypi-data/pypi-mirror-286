from .tracking import *
from .val import workload_name, url
from .integration.keras import LoggingCallback
from .integration.pytorchLightning import TorchLoggingCallback
from .tracking import LoggingClient

__version__ = '0.0.1'

__all__ = (
    'log'
    'LoggingCallback'
    'TorchLoggingCallback'
)


def log(log_data: Dict):
    client = LoggingClient()
    client.log(log_data)
