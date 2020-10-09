from abc import ABCMeta, abstractmethod
from time import sleep
from typing import Dict, List
import json
import logging
import os
import sys

from ._base import Base
from .producer import Producer

sqspy_logger = logging.getLogger("sqs_py")


class Consumer(Base):
    __metaclass__ = ABCMeta
    WAIT_TIME = 0
    POLL_INTERVAL = 60
    MAX_MESSAGES_COUNT = 1

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
        error_queue_data: Dict = {
            "name": kwargs.get("error_queue"),
            "url": kwargs.get("error_queue_url"),
            "visibility_timeout": kwargs.get("error_visibility_timeout"),
        }
        self._poll_interval: int = int(kwargs.get("interval", self.POLL_INTERVAL))
        self._message_attribute_names: List = kwargs.get("message_attribute_names", [])
        self._attribute_names: List = kwargs.get("attribute_names", [])
        self._wait_time: int = int(kwargs.get("wait_time", self.WAIT_TIME))
        self._max_number_of_messages: int = int(
            kwargs.get("max_number_of_messages", self.MAX_MESSAGES_COUNT)
        )
        self._force_delete: bool = kwargs.get("force_delete", False)
        self._queue = queue or self.get_queue(queue_data)
        if self.queue is None:
            raise ValueError(
                "No queue found with name or URL provided, or "
                "application did not have permission to create one."
            )
        self._queue_name = self._queue.url.split("/")[-1]
        self._error_queue = None
        if error_queue_data.get("name") or error_queue_data.get("url"):
            self._error_queue = Producer(
                queue_name=error_queue_data.get("name"),
                queue_url=error_queue_data.get("url"),
                queue=self.get_queue(error_queue_data),
            )
            #self._error_queue_name = self._error_queue.url.split("/")[-1]
            self._error_queue_name = self._error_queue.queue_name

    @property
    def queue(self):
        return self._queue

    @property
    def queue_name(self):
        return self._queue_name

    def poll_messages(self):
        while True:
            messages = self._queue.receive_messages(
                AttributeNames=self._attribute_names,
                MessageAttributeNames=self._message_attribute_names,
                WaitTimeSeconds=self._wait_time,
                MaxNumberOfMessages=self._max_number_of_messages,
            )
            if not messages:
                sqspy_logger.debug(
                    f"No messages were fetched for {self.queue_name}. "
                    f"Sleeping for {self._poll_interval} seconds."
                )
                sleep(self._poll_interval)
                continue
            sqspy_logger.info(
                f"{len(messages)} messages received for {self.queue_name}"
            )
            break
        return messages

    def _start_listening(self):
        while True:
            messages = self.poll_messages()
            for message in messages:
                m_body = message.body
                message_attribs = message.message_attributes
                attribs: Dict = message.attributes
                # catch problems with malformed JSON, usually a result
                # of someone writing poor JSON directly in the AWS
                # console
                try:
                    body = json.loads(m_body)
                except:
                    sqspy_logger.warning(
                        f"Unable to parse message - JSON is not formatted properly. "
                        f"Received message: {m_body}"
                    )
                    continue
                try:
                    if self._force_delete:
                        message.delete()
                        self.handle_message(body, message_attribs, attribs)
                    else:
                        self.handle_message(body, message_attribs, attribs)
                        message.delete()
                except Exception as ex:
                    # need exception logtype to log stack trace
                    sqspy_logger.exception(ex)
                    if self._error_queue:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        sqspy_logger.info("Pushing exception to error queue")
                        self._error_queue.publish(
                            {
                                "exception_type": str(exc_type),
                                "error_message": str(ex.args),
                            }
                        )

    def listen(self):
        sqspy_logger.info(f"Listening to queue {self.queue_name}")
        if self._error_queue:
            sqspy_logger.info(f"Using error queue {self._error_queue_name}")
        self._start_listening()

    @abstractmethod
    def handle_message(self, body, attributes, messages_attributes):
        raise NotImplementedError("Implement this function in subclass.")
