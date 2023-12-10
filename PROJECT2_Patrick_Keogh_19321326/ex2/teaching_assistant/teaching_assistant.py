import sys, os, json
import time

from rabbitmq_setup import setup_rabbitmq, wait_for_start_signal

def main():
    channel = setup_rabbitmq()

    wait_for_start_signal(channel, 'ta')

    def callback(ch, method, properties, body):
        assignment = json.loads(body)
        print(f"Received assignment from student {assignment['StudentID']} with status {assignment['status']}")
        if assignment["status"] == "corrected":
            assignment["status"] = "validated"
            print(f"Validating assignment from student {assignment['StudentID']} and sending back to exchange")
            channel.basic_publish(
                exchange="assignment_exchange",
                routing_key="result_queue",
                body=json.dumps(assignment),
            )
            print(f"Assignment from student {assignment['StudentID']} sent to result_queue")
            signal_message = json.dumps({"signal": "start"})
            channel.basic_publish(exchange='', routing_key='start_signal_queue_mc', body=signal_message)

    channel.basic_consume(
        queue="validation_queue", on_message_callback=callback, auto_ack=False
    )

    print(" [*] Teaching assistant is Waiting...")
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
