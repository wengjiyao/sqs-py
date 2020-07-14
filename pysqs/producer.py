import json
import logging
import os

from .base import Base

pysqs_logger = logging.getLogger("pysqs")


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
            "visibility_timeout": kwargs.get("error_visibility_timeout"),
        }
        self._queue = queue or self.get_or_create_queue(
            queue_data, create_queue=kwargs.get("create_queue"),
        )
        if self._queue is None:
            raise ValueError(
                "No queue found with name or URL provided, or "
                "application did not have permission to create one."
            )
        self._queue_name = self._queue.url.split("/")[-1]

    def publish(self, message, **kwargs):
        pysqs_logger.info(f"Sending message to queue.")
        return self._queue.send_message(MessageBody=json.dumps(message), **kwargs)
