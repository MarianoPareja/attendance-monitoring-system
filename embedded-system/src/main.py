import threading
from collections import deque
from datetime import datetime

from config import (
    CAMERA_SOURCE,
    CLASSROOM_ID,
    COURSE_SCHEDULE_ENDPOINT,
    FRAME_INTERVAL,
    SERVER_ENDPOINT,
)
from utils.ImageProcessing import get_faces
from utils.Scheduler import SubjectsScheduler
from utils.Sender import send_information
from utils.VideoCapture import capture_image

lock = threading.Lock()
main_queue = deque()


def manage_data(exit_flag):
    """
    Manages process and send the data to the server
    """
    while not exit_flag:
        try:
            if main_queue:
                with lock:
                    image, time = main_queue.pop()
                    faces = get_faces(image)
                send_information(faces, CLASSROOM_ID, time, SERVER_ENDPOINT)
        except Exception as e:
            print("Error {}".format(e))


def control_schedules(end_time: datetime):
    """
    Controls the schedule's times
    """

    exit_flag = False

    worker_1 = threading.Thread(
        target=capture_image(
            camera_source=CAMERA_SOURCE,
            frame_interval=FRAME_INTERVAL,
            images_queue=main_queue,
        ),
        args=(exit_flag,),
    )

    worker_2 = threading.Thread(target=manage_data, args=(exit_flag,))

    worker_1.start()
    worker_2.start()

    worker_1.join()
    worker_2.join()

    while datetime.now() < end_time:
        pass

    exit_flag = True

    print("Exiting at time {}".format(datetime.now().strftime("%Y:%m:%d:%H:%M:%S")))


if __name__ == "__main__":
    scheduler = SubjectsScheduler(COURSE_SCHEDULE_ENDPOINT)
    scheduler.get_schedule(CLASSROOM_ID)
    scheduler.generate_schedule(control_schedules)
