from typing import List

from pydantic import BaseModel


class DetectionData(BaseModel):
    time: str
    course_id: str
    faces: List[List[float]]
