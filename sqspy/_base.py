from os import getenv
from typing import Dict
import logging

import boto3
import boto3.session

sqspy_logger = logging.getLogger("sqspy")


class Base:
    QUEUE_VISIBILITY_TIMEOUT = "600"

    def __init__(self, **kwargs):
        aws_access_key_id = kwargs.get("aws_access_key_id")
        aws_secret_access_key = kwargs.get("aws_secret_access_key")
        profile_name = kwargs.get("profile_name")
        endpoint_url = kwargs.get("endpoint_url")
        region_name = kwargs.get("region_name")
        self._session = boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            profile_name=profile_name,
            region_name=region_name,
        )
        self._sqs = self._session.resource(
            "sqs",
            region_name=region_name,
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        sqspy_logger.debug("Initialised SQS resource")

    def get_or_create_queue(self, queue_data: Dict, create_queue: bool = True):
        queue_name = queue_data.get("name")
        queue_visibility: str = queue_data.get("visibility_timeout") or self.QUEUE_VISIBILITY_TIMEOUT
        queue = self.get_queue(queue_data)
        if queue is not None:
            return queue
        if create_queue is False:
            sqspy_logger.warning("Denied creation of queue.")
            return None
        sqspy_logger.debug(f"Creating the queue: {queue_name}")
        queue_attributes = {
            "VisibilityTimeout": queue_visibility,
        }
        if queue_name.endswith(".fifo"):
            queue_attributes["FifoQueue"] = "true"
        return self.create_queue(queue_name, queue_attributes)

    def get_queue(self, queue_data: Dict):
        queue_url = queue_data.get("url")
        queue_name = queue_data.get("name")
        if queue_url:
            return self._sqs.Queue(queue_url)
        for q in self._sqs.queues.filter(QueueNamePrefix=queue_name):
            name = q.url.split("/")[-1]
            if name == queue_name:
                return q
        sqspy_logger.warning("Queue not found.")
        return None

    def create_queue(self, name: str, attributes: Dict):
        return self._sqs.create_queue(QueueName=name, Attributes=attributes)
