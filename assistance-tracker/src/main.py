import json
import threading
import time
from datetime import datetime, timedelta

from connections.rabbitmq import RabitMQConnection
from models.assistanceTracker import AssistanceTracker

assist_tracker_list = []
rabbitmq_conn = RabitMQConnection(
    host="localhost", exchange="direct_data", exchange_type="direct"
)


def class_exists(class_id):
    for index, class_tracker in enumerate(assist_tracker_list):
        if class_tracker.class_id == class_id:
            return index

    return None


def create_assistance_tracker(class_id):
    class_tracker = AssistanceTracker(class_id=class_id)
    schedule_response = class_tracker.get_class_schedule()
    embeddings_respoonse = class_tracker.get_class_embeddings()

    if not schedule_response or not embeddings_respoonse:
        return None

    assist_tracker_list.append(class_tracker)

    return len(assist_tracker_list) - 1


def callback(ch, method, properties, body):
    data = json.loads(body)
    class_id = data.get("class_id", None)

    tracker_index = class_exists(class_id)
    if tracker_index is None:
        tracker_index = create_assistance_tracker(class_id)
        if tracker_index is None:
            return

    class_tracker = assist_tracker_list[tracker_index]

    class_tracker.detect_student(data.get("embeddings", []))


def check_class_schedules():
    for index, class_tracker in enumerate(assist_tracker_list):
        aux_time = datetime.now() + timedelta(minutes=38)
        if (
            datetime.now().time()
            > (class_tracker.end_time + timedelta(minutes=24)).time()
        ):
            class_tracker.post_assistance_record()
            assist_tracker_list.pop(index)


def thread_1():
    while True:
        check_class_schedules()
        time.sleep(5)


def thread_2():
    while True:
        rabbitmq_conn.consume_messages(callback_fn=callback)


if __name__ == "__main__":
    thread1 = threading.Thread(target=thread_1)
    thread2 = threading.Thread(target=thread_2)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
