import pika
import os


def setup_rabbitmq():
    # Establish a connection to RabbitMQ
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("rabbitmq", 5672, "/", credentials)
    )
    channel = connection.channel()

    # Declare exchanges and queues
    channel.exchange_declare(exchange="assignment_exchange", exchange_type="direct")
    queues = [
        "data_mining_queue",
        "cloud_computing_queue",
        "validation_queue",
        "result_queue",
    ]
    for queue in queues:
        channel.queue_declare(queue=queue)
        channel.queue_bind(exchange="assignment_exchange", queue=queue)

    return channel
