from typing import List

from pydantic import BaseModel


class DetectionData(BaseModel):
    time: str
    class_id: int
    faces: List[List[List[int]]]
