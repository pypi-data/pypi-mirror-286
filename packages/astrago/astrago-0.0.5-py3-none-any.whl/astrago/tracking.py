from typing import Dict

from .dataSender import DataSender
from .val import *
import atexit


class LoggingClient:
    def __init__(self):
        self.sender = DataSender()
        self.uuid = uuid
        self.user_id = user_id
        self.base_url = url
        self.start_time = time.time()
        self.step = 0
        self.epoch = 0
        self.workload_name = workload_name
        self.train_data = None
        self.log_data = []
        atexit.register(self._flush_logs)

    def log(self, log_data: Dict):
        self.step += 1
        if self.step % 10 == 0:
            request_data = {
                "step": self.step,
                "epochs": self.epoch,
                "relativeTime": self.__calculate_relative_time__(),
                "wallTime": time.time(),
                "log": log_data
            }

            self.log_data.append(request_data)

        if len(self.log_data) >= 1000:
            self._flush_logs()

    def _flush_logs(self):
        if len(self.log_data) > 0:
            self.train_data = {
                "uuid": self.uuid,
                "workloadName": self.workload_name,
                "userId": self.user_id,
                "metrics": self.log_data
            }
            try:
                self.sender.send_metric(self.train_data)
            except Exception as e:
                print(f"Failed to send metrics: {e}")
            finally:
                self.log_data = []

    def __del__(self):
        print('del')
        self._flush_logs()

    def __calculate_relative_time__(self):
        return time.time() - self.start_time
