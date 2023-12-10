import sys, os, json
import time

from rabbitmq_setup import setup_rabbitmq, wait_for_start_signal

def main():
    channel = setup_rabbitmq()

    wait_for_start_signal(channel, 'mc')

    def callback(ch, method, properties, body):
        assignment = json.loads(body)
        print(f"Received assignment from student {assignment['StudentID']} with status {assignment['status']}")
        if assignment["status"] == "validated":
            print(f"Publishing assignment from student {assignment['StudentID']} to Brightspace")
            assignment["status"] = "published"
            channel.basic_publish(exchange='assignment_exchange', routing_key='', body=json.dumps(assignment))
            print(f"Assignment from student {assignment['StudentID']} published to Brightspace")

    channel.basic_consume(queue="result_queue", on_message_callback=callback, auto_ack=False)
    print(" [*] Module Coordinator is Waiting...")
    channel.start_consuming()

if __name__ == "__main__":
    time.sleep(20)
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

