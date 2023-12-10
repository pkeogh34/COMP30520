import json
import os
import sys
import time

from rabbitmq_setup import setup_rabbitmq

def send_assignments(assignments):
    channel = setup_rabbitmq()

    for assignment in assignments:
        assignment_json = json.dumps(assignment)
        routing_key = f"{assignment['module']}_queue"
        channel.basic_publish(exchange='assignment_exchange', routing_key=routing_key, body=assignment_json)
        print(f"Assignment from student {assignment['StudentID']} for {assignment['module']} sent for correction")

    channel.connection.close()

def collect_assignments():
    # Dummy input to ensure the first prompt displays correctly
    input("")
    print("Welcome to the Assignment Submission System!")
    assignments = []

    while True:
        print("\nPlease enter the assignment details")
        student_id = input("Enter student ID: ")
        module = input("Enter the module: ")
        answer = input("Enter the content of the answer: ")

        assignment = {
            "StudentID": student_id,
            "module": module,
            "answer": answer,
            "status": "submitted",
        }
        assignments.append(assignment)

        while True:
            choice = input("Do you want to publish all assignments? (Y/N): ").strip().lower()
            print("\n")
            if choice in ["y", "yes"]:
                return assignments
            elif choice in ["n", "no"]:
                break
            else:
                print("Invalid input. Please enter 'Y' for Yes or 'N' for No")

def send_start_signal():
    channel = setup_rabbitmq()
    signal_message = json.dumps({"signal": "start"})
    channel.basic_publish(exchange='', routing_key='start_signal_queue_dm', body=signal_message)
    channel.basic_publish(exchange='', routing_key='start_signal_queue_cc', body=signal_message)
    print("Start signal sent to demonstrators\n")

    while True:
        choice = input("Do you wish to exit the program? (Y/N): ").strip().lower()
        if choice in ["y", "yes"]:
            print("Exiting the program.")
            sys.exit(0)
        elif choice in ["n", "no"]:
            return
        else:
            print("Invalid input. Please enter 'Y' for Yes or 'N' for No")

def main():
    while True:
        assignments = collect_assignments()
        if assignments:
            send_assignments(assignments)
            send_start_signal()
        else:
            print("No assignments to send")

if __name__ == "__main__":
    print("Waiting for RabbitMQ to start up...")
    time.sleep(20)
    print("Press Enter to start...")

    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)





