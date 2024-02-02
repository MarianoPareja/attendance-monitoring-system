import json
import logging
import os
from typing import List

from fastapi import APIRouter, Response
from pydantic import BaseModel
from torch import Tensor

from connections.rabbitmq import RabitMQConnection
from models.InceptionResnetV1 import InceptionResnetV1, load_weights

logging.basicConfig(level=logging.DEBUG)

emb_router = APIRouter()

rabbitmq_conn = RabitMQConnection(
    host="localhost", exchange="direct_data", exchange_type="direct"
)

model = InceptionResnetV1().eval()
load_weights(
    model,
    "/Users/mariano/Documents/Projects/attendance-monitoring-system/embeddings-extraction/models/20180402-114759-vggface2.pt",
)


class DetectionData(BaseModel):
    time: str
    class_id: int
    faces: List[List[List[int]]]


@emb_router.post("/detected_faces")
async def extract_embeddings(data: DetectionData):
    """
    Recieves json containing the detected faces and generates embeddings of them.
    Input Json Structure:
    {
        "time": str,
        "class_id": str,
        "faces": list,
    }
    """
    print("ENTERED THE 'extract_embeddings' FUNCTION")
    # print(data)

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
        rabbitmq_conn.post_message(data=embeddings_data, routing_key="embeddings")

        # Upload data to 'Embedding Queue'

        return Response(status_code=200)

    except Exception as e:
        print(f"Exception: {str(e)}")
        return Response(content=str(e), status_code=422)
