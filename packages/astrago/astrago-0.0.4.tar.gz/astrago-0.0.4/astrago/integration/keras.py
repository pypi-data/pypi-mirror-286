import tensorflow as tf
from ..dataSender import DataSender
from ..val import *


class LoggingCallback(tf.keras.callbacks.Callback):
    def __init__(self):
        super(LoggingCallback, self).__init__()
        self.sender = None
        self.uuid = uuid
        self.user_id = user_id
        self.base_url = url
        self.start_time = time.time()
        self.step = 0,
        self.epoch = 0,
        self.workload_name = workload_name
        self.train_data = None
        self.log_data = []

    def on_epoch_begin(self, epoch, logs=None):
        self.epoch = epoch + 1

    def on_train_begin(self, logs=None):
        self.sender = DataSender()
        # 학습 시작시 step 초기화
        self.step = 0
        self.epoch = 0
        self.log_data = []
        self.train_data = {
            "uuid": self.uuid,
            "workloadName": self.workload_name,
            "userId": self.user_id,
            "metrics": self.log_data
        }

    def on_train_batch_end(self, batch, logs=None):
        self.step += 1
        if self.step % 10 == 0:
            request_data = {
                "step": self.step,
                "epochs": self.epoch,
                "relativeTime": self.__calculate_relative_time__(),
                "wallTime": time.time(),
                "log": logs
            }
            self.log_data.append(request_data)
        if len(self.log_data) >= 1000:
            # 데이터 발송
            self.send_metrics()

    def on_train_end(self, logs=None):
        if len(self.log_data) >= 0:
            self.send_metrics()

    def __calculate_relative_time__(self):
        return time.time() - self.start_time

    def send_metrics(self):
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