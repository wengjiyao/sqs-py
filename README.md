# sqspy

Forked from [the sqspy][1] package and removed sqs list_queues.

## Install

```Shell
pip install sqs_py
```

## Usage

```Python
from sqs_py import Consumer


class MyWorker(Consumer):
    def handle_message(self, body, attributes, message_attributes):
        print(body)


listener = MyWorker('Q1', error_queue='EQ1')
listener.listen()
```

More documentation coming soon.

## Why

SQS list_queues conflicts with the permission in my AWS environment.

Support python 3.6+


[1]: https://pypi.org/project/sqspy/ "sqspy on PyPI"
