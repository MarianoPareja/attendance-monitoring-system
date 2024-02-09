import json
from datetime import datetime

import requests


def send_information(faces, class_id, time, server_endpoint):
    """
    Sent JSON data about embeddings and class to the server

    Arguments:
    :param faces(list): List containing reshape images of faces with shape (number of images, wiidth height, channels)
    :param class_id(int): Class identifier
    :param time(datetime): Object specifying the time the frame was captured
    """
    try:
        data = {
            "time": time.strftime("%H-%M-%S"),
            "class_id": class_id,
            "faces": faces,
        }
        # Stablish connection with the server
        data = json.loads(faces)
        requests.post(server_endpoint, data)

    except Exception as e:
        raise e
