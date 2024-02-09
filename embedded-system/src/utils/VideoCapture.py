import json
from datetime import datetime, timedelta
from time import sleep

import cv2


def capture_image(camera_source, frame_interval, images_queue, exit_flag):
    """
    Function to capture images and time of the image

    :pararm camera_source(int): Camera input identifier
    :param frame_interval(int): Time in milliseconds between each frame
    :images_queue(list): List to store data tuples (image, datetime)
    """

    if not isinstance(camera_source, int):
        raise ValueError("cammera_source must be a int indicating the camera indice")

    # Create VideoCapture instance
    capture = cv2.VideoCapture(camera_source)

    if not capture.isOpened():
        raise ValueError(
            "Camera with indice {} could not be opened. Make sure camera exists and is available".format(
                camera_source
            )
        )

    capture_time = datetime.now()

    while not exit_flag:

        if datetime.now() >= capture_time + timedelta(microseconds=frame_interval):

            # Update capture time
            capture_time = datetime.now()

            # Make sure an image is read
            ret = False
            while not ret:
                ret, image = capture.read()

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Send image to a new thread
            images_queue.append((image, capture_time))

            sleep(frame_interval / 60)
