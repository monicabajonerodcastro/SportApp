from concurrent import futures
from google.cloud import pubsub_v1
from typing import Callable

project_id = "poc-uniandes-416200"
topic_id = "alertas"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)
publish_futures = []

def get_callback(
    publish_future: pubsub_v1.publisher.futures.Future, data: str
) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
    def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
        try:
            print(publish_future.result(timeout=60))
        except futures.TimeoutError:
            print(f"Timeout al publicar el mensaje [{data}].")

    return callback

def publicar_mensaje(mensaje: str):
    
    publish_future = publisher.publish(topic_path, mensaje.encode("utf-8"))
    publish_future.add_done_callback(get_callback(publish_future, mensaje))
    publish_futures.append(publish_future)

    futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

    #print(f"Published messages with error handler to {topic_path}.")