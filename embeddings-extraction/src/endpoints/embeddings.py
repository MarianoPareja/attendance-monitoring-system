import json
import logging
import time
from typing import List

from fastapi import APIRouter, Response
from pika.exceptions import AMQPConnectionError
from pydantic import BaseModel
from torch import Tensor

from connections.rabbitmq import RabitMQConnection
from models.detectionData import DetectionData
from models.InceptionResnetV1 import InceptionResnetV1, load_weights

logging.basicConfig(level=logging.DEBUG)


# CONSTANTS DECLARATION
# ------------------------------------------

RABBITMQ_HOST = "localhost"
EXHCANGE_NAME = "direct_data"
EXHCANGE_TYPE = "direct"
WEIGHTS_FILE_PATH = "/Users/mariano/Documents/Projects/attendance-monitoring-system/embeddings-extraction/models/20180402-114759-vggface2.pt"


# COMPONENTS INITIALIZATION
# ------------------------------------------

emb_router = APIRouter()
rabbitmq_conn = RabitMQConnection(
    host=RABBITMQ_HOST, exchange=EXHCANGE_NAME, exchange_type=EXHCANGE_TYPE
)
model = InceptionResnetV1().eval()
load_weights(model, WEIGHTS_FILE_PATH)


# ROUTES DEFINITION
# ------------------------------------------


@emb_router.post("/detected_faces")
async def extract_embeddings(data: DetectionData):
    """
    Recieves json containing the detected faces and generates embeddings of them.

    Parameters:
    - data (DetectionData): Json formatted data including ("time", "class_id", "embeddings") of detected faces

    Returns:
    HTTP Response Code

    """

    try:
        tensor = Tensor(data.faces)
        if len(tensor.shape) != 4:
            tensor = tensor.unsqueeze(0)

        tensor = tensor.permute(0, 3, 1, 2)

        embeddings = model.forward(tensor)
        embeddings = embeddings.tolist()

        embeddings_data = {
            "time": data.time,
            "class_id": data.class_id,
            "embeddings": embeddings,
        }
        embeddings_data = json.dumps(embeddings_data)

        try:
            rabbitmq_conn.post_message(data=embeddings_data, routing_key="embeddings")
        except:
            logging.error(f"AMQPConnectionError: {str(e)}")
            logging.info("Attempting to reconnect to RabbitMQ...")
            time.sleep(3)

        return Response(status_code=200)

    except ValueError as ve:
        logging.error(f"ValueError: {str(ve)}")
        return Response(content=str(ve), status_code=422)

    except Exception as e:
        logging.error(f"Exception: {str(e)}")
        return Response(content=str(e), status_code=500)
