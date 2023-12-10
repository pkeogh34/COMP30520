import json

import pika
import time

def setup_rabbitmq():
    max_retries = 5
    retry_delay = 5  # seconds
    for attempt in range(max_retries):
        try:
            # Establish a connection to RabbitMQ
            credentials = pika.PlainCredentials('guest', 'guest')
            connection = pika.BlockingConnection(
                pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
            )
            channel = connection.channel()

            # Declare exchanges and queues
            channel.exchange_declare(exchange='assignment_exchange', exchange_type='direct')
            queues = [
                'data_mining_queue',
                'cloud_computing_queue',
                'validation_queue',
                'result_queue',
                'start_signal_queue_dm',
                'start_signal_queue_cc',
                'start_signal_queue_ta',
                'start_signal_queue_mc',
            ]
            for queue in queues:
                channel.queue_declare(queue=queue)
                if queue not in ['start_signal_queue_dm', 'start_signal_queue_cc','start_signal_queue_ta','start_signal_queue_mc']:
                    channel.queue_bind(exchange='assignment_exchange', queue=queue)

            return channel
        except pika.exceptions.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                print(f"Connection failed, retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Maximum retries reached. Could not connect to RabbitMQ.")
                raise

def wait_for_start_signal(channel, module):
    for method_frame, properties, body in channel.consume(f'start_signal_queue_{module}', auto_ack=True):
        signal = json.loads(body)
        if signal.get("signal") == "start":
            print("Received start signal. Beginning to process assignments.")
            break
        time.sleep(1)  # Sleep to prevent busy waiting