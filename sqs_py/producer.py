import json
import logging
import os

from ._base import Base

sqspy_logger = logging.getLogger("sqs_py")


class Producer(Base):
    def __init__(self, queue_name: str = None, queue_url: str = None, **kwargs):
        queue = kwargs.get("queue")
        if not any([queue, queue_name, queue_url]):
            raise ValueError(
                "One of `queue`, `queue_name` or `queue_url` should be provided"
            )
        super().__init__(**kwargs)
        queue_data: Dict = {
            "name": queue_name,
            "url": queue_url,
            "visibility_timeout": kwargs.get("visibility_timeout"),
        }
        self._queue = queue or self.get_or_create_queue(
            queue_data, create_queue=kwargs.get("create_queue"),
        )
        if self.queue is None:
            raise ValueError(
                "No queue found with name or URL provided, or "
                "application did not have permission to create one."
            )
        self._queue_name = self._queue.url.split("/")[-1]

    @property
    def queue(self):
        return self._queue

    @property
    def queue_name(self):
        return self._queue_name

    def publish(self, message, **kwargs):
        sqspy_logger.info(f"Sending message to queue {self.queue_name}.")
        return self._queue.send_message(MessageBody=json.dumps(message), **kwargs)
