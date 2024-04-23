import os
from google.cloud import pubsub_v1

_ENVIRONMENT = os.environ["ENVIRONMENT"]

class PublicadorMensajes:
    def __init__(self, project_id: str, topic_id: str) -> None:
        self.publisher = pubsub_v1.PublisherClient()
        self. topic_path = self.publisher.topic_path(project_id, topic_id)

    def publicar_mensaje(self, message: str):
        if _ENVIRONMENT == "test":
            return 0
        data = message.encode("utf-8")
        future = self.publisher.publish(self.topic_path, data)
        return future.result()
