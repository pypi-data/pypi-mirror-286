from .tracking import *
from .val import workload_name, url
from .tracking import LoggingClient

__version__ = '0.0.4'

__all__ = (
    'log'
)


def log(log_data: Dict):
    client = LoggingClient()
    client.log(log_data)
