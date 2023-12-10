import sys, os, json
from rabbitmq_setup import setup_rabbitmq


def main():
    channel = setup_rabbitmq()

    def callback(ch, method, properties, body):
        assignment = json.loads(body)
        print(f"Received assignment from student {assignment['StudentID']} with status {assignment['status']}")
        if assignment["status"] == "corrected":
            assignment["status"] = "validated"
            channel.basic_publish(
                exchange="assignment_exchange",
                routing_key="result_queue",
                body=json.dumps(assignment),
            )
        print(f"Assignment from student {assignment['StudentID']} sent to result_queue")

    channel.basic_consume(
        queue="validation_queue", on_message_callback=callback, auto_ack=False
    )

    print(" [*] Teaching assistant is Waiting...")
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
