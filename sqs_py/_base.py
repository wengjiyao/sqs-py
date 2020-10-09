from os import getenv
from typing import Dict
import logging

import boto3
import boto3.session

sqspy_logger = logging.getLogger("sqs_py")


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

    def get_queue(self, queue_data: Dict):
        queue_name = queue_data.get("name")
        queue_visibility: str = queue_data.get("visibility_timeout") or self.QUEUE_VISIBILITY_TIMEOUT

        queue_url = queue_data.get("url")
        queue_name = queue_data.get("name")
        if queue_url:
            return self._sqs.Queue(queue_url)

        return self._sqs.get_queue_by_name(QueueName=queue_name)

