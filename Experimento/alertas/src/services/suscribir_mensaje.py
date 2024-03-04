from concurrent import futures
from google.cloud import pubsub_v1
from typing import Callable

project_id = "poc-uniandes-416200"
subscription_id = "alertas-sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)
timeout = 5.0

def callback(message: pubsub_v1.subscriber.message.Message):
    print("============= Mensaje recibido ================")
    print(message.data)
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print("====================== Esperando mensajes ... ======================")

with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
