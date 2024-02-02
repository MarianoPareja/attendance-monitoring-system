import json
from datetime import datetime, time

import numpy as np
import requests


def cosine_similarity(embeddings_truth, embeddings_input):
    emb_truth_np = np.array(embeddings_truth)
    emb_input_np = np.array(embeddings_input)

    dot_product = np.dot(emb_truth_np, emb_input_np.T)

    norm_truth = np.linalg.norm(emb_truth_np, axis=1)
    norm_input = np.linalg.norm(emb_input_np, axis=1)

    similarity = dot_product / (np.outer(norm_truth, norm_input) + 1e-8)

    return similarity.tolist()


class AssistanceTracker:
    def __init__(self, class_id, threshold=0.8):
        self.class_id = class_id
        self.start_time = None
        self.end_time = None
        self.students = []  # List containing {"student_id": int, "record": list}
        self.embeddings = []
        self.threshold = threshold

    def get_class_schedule(self):
        """
        Get start_time and end_time as datetime.datetime objects
        """
        weekday = datetime.now().isoweekday()
        response = requests.get(
            f"http://localhost:8000/api/v1/class_schedule/{self.class_id}/{weekday}"
        )
        data = response.json()

        if not data:
            return False

        date_str_format = "%H:%M:%S"

        self.start_time = datetime.strptime(data[0]["start_time"], date_str_format)
        self.end_time = datetime.strptime(data[0]["end_time"], date_str_format)

        return True

    def get_class_embeddings(self):
        """
        Get all the embeddings of the students enrolled in this class
        """
        response = requests.get(
            f"http://localhost:8000//api/v1/class_embeddings/{self.class_id}"
        )
        data = response.json()

        if not data:
            return False

        for student_data in data:
            self.students.append({"student_id": student_data["student"], "record": []})
            self.embeddings.append(student_data["embedding"])

        return True

    def detect_student(self, students_embeddings):
        """
        Compare students_embeddings and add similarities to list

        args:
            students_embeddings: list of embeddings of detected faces
        outputs:
            None
        """
        actual_time = datetime.now()
        similarity = cosine_similarity(self.embeddings, students_embeddings)
        for index, row in enumerate(similarity):
            if (np.array(row) > self.threshold).any():
                self.students[index]["record"].append(actual_time)

    def post_assistance_record(self):
        date = datetime.now().date()
        attendance_control = []
        for student in self.students:
            attendance_control.append(
                {
                    "date": date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "assistance": len(student.get("record", [])) > 10,
                    "subject": self.class_id,
                    "student": student.get("student_id"),
                }
            )
        json_data = json.dumps(attendance_control)

        headers = {"Content-Type": "application/json"}

        response = requests.post(
            "http://localhost:8000/api/v1/attendance_control_list",
            headers=headers,
            data=json_data,
        )

        print(response)

        return response
