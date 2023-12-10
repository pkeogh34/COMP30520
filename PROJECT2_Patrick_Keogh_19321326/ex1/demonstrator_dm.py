import sys, os, json
from rabbitmq_setup import setup_rabbitmq


def main():
    channel = setup_rabbitmq()

    def callback(ch, method, properties, body):
        assignment = json.loads(body)
        print(f"Received assignment from student {assignment['StudentID']} with status {assignment['status']}")
        if assignment["status"] == "submitted":
            assignment["status"] = "corrected"
            channel.basic_publish(
                exchange="assignment_exchange",
                routing_key="validation_queue",
                body=json.dumps(assignment),
            )
        print(f"Assignment from student {assignment['StudentID']} sent to validation_queue")

    channel.basic_consume(
        queue="data_mining_queue", on_message_callback=callback, auto_ack=False
    )
    print(" [*] Demonstrator is Waiting...")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
