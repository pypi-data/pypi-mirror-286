from typing import Any

import pytorch_lightning as pl

from lightning.pytorch.utilities.types import STEP_OUTPUT

from ..val import *
import lightning as L


class TorchLoggingCallback(L.Callback):
    def __init__(self):
        super(TorchLoggingCallback, self).__init__()
        self.sender = None
        self.uuid = uuid
        self.user_id = user_id
        self.base_url = url
        self.start_time = time.time()
        self.step = 0
        self.epoch = 0
        self.workload_name = workload_name
        self.train_data = None
        self.log_data = []

    def on_train_epoch_start(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule"):
        self.epoch = trainer.current_epoch + 1

    def on_train_batch_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule", outputs: STEP_OUTPUT,
                           batch: Any, batch_idx: int):
        self.step += 1
        if self.step % 10 == 0:
            loss = outputs['loss'].item() if 'loss' in outputs and hasattr(outputs['loss'], 'item') else None
            accuracy = pl_module.accuracy.compute().item() if hasattr(pl_module, 'accuracy') and hasattr(
                pl_module.accuracy, 'compute') else None

            if loss is None or accuracy is None:
                print(f"Error: Loss or accuracy is None. Loss: {loss}, Accuracy: {accuracy}")

            request_data = {
                "step": self.step,
                "epochs": self.epoch,
                "relativeTime": self.__calculate_relative_time__(),
                "wallTime": time.time(),
                "log": {
                    "loss": loss,
                    "accuracy": accuracy
                }
            }
            self.log_data.append(request_data)
        if len(self.log_data) >= 1000:
            self.send_metrics()

    def on_train_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
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
