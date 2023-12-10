import json, os
from rabbitmq_setup import setup_rabbitmq

channel = setup_rabbitmq()


def publish_assignment(id, module, answer):
    assignment = json.dumps(
        {
            "StudentID": id,
            "module": module,
            "answer": answer,
            "status": "submitted",
        }
    )

    channel.basic_publish(
        exchange="assignment_exchange", routing_key=f"{module}_queue", body=assignment
    )
    print(f"Assignment of student {id} sent for correction")


publish_assignment(1932, "data_mining", "some answers, probably correct")
publish_assignment(1326, "cloud_computing", "some answers, probably correct")


channel.connection.close()
