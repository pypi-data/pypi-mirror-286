import logging
from typing import Optional
import requests
from urllib.parse import urljoin

class Handler(logging.Handler):
    def __init__(self, endpoint: str, namespace: str, topic: str):
        super().__init__(logging.DEBUG)
        self.endpoint = endpoint
        self.namespace = namespace
        self.topic = topic

    def emit(self, record: logging.LogRecord):
        post_endpoint = urljoin(self.endpoint, 'create')
        data = {
            "namespace": self.namespace,
            "topic": self.topic,
            "data": record.getMessage(),
            "level": record.levelname
        }
        requests.post(post_endpoint, json=data)

class Logger(logging.Logger):
    def __init__(self, endpoint: str, namespace: Optional[str] = None, topic: Optional[str] = None):
        self.endpoint = endpoint
        self.namespace = "default" if namespace is None else namespace
        self.topic = "default" if topic is None else topic
        self.handler = Handler(self.endpoint, self.namespace, self.topic)
        super().__init__(self.topic, logging.DEBUG)
        self.addHandler(self.handler)


    def getChild(self, suffix: str) -> 'Logger':
        child = Logger(self.endpoint, self.namespace, self.topic + '_' + self.name)
        return child
