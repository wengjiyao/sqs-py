# pysqs

A more pythonic approach to SQS producer/consumer utilities. Heavily
inspired (or complete rewrite) or [the pySqsListener][1] package.

## Install

```Shell
pip install pysqs
```

## Usage

```Python
from pysqs import Consumer


class MyWorker(Consumer):
    def handle_message(self, body, attributes, message_attributes):
        print(body)

listener = MyWorker('Q1', error_queue='EQ1')
listener.listen()
```

More documentation coming soon. Although, `pySqsListener` users can switch class imports as follows:

 * `sqs_listener.SqsListener` -> `pysqs.Consumer`
 * `sqs_launcher.SqsLauncher` -> `pysqs.Producer`


[1]: https://pypi.org/project/pySqsListener/ "pySqsListener on PyPI"
