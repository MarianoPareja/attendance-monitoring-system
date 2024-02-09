import json
from collections import defaultdict

import requests
import schedule


class SubjectsScheduler:

    def __init__(self, course_schedule_endpoint):
        self.scheduler = schedule.Scheduler()
        self.schedule_data = None
        self.course_schedule_endpoint = course_schedule_endpoint

    def get_schedule(self, classroom_id):
        """
        Gets all schedules jobs based on class schedule for specific classroom ID.

        :param classroom_id(int): Clasroom identifier in the database

        """
        try:
            response = requests.get(self.course_schedule_endpoint, classroom_id)
            if response.status_code == 404:
                return None
            data = json.loads(response.content)

            self.schedule_data = defaultdict(list)

            for schedule in data:
                schedule_weekday = str(schedule.get("weekday"))
                self.schedule_data[schedule_weekday].append(
                    (schedule.get("start_time"), schedule.get("end_time"))
                )

        except Exception as e:
            print(Exception)

    def generate_schedule(self, func):
        """
        Generates schedule bases on data stracted from the database

        :param func: Function to be called by every schedule job

        """

        for day, day_schedule in self.schedule_data.items():
            if day == "1":  # Monday
                for class_schedule in day_schedule:
                    self.scheduler.every().monday.at(class_schedule[0]).do(
                        func(class_schedule[1])
                    )

            elif day == "2":  # Tuesday
                for class_schedule in day_schedule:
                    self.scheduler.every().tuesday.at(class_schedule[0]).do(
                        func(class_schedule[1])
                    )

            elif day == "3":  # Wednesday
                for class_schedule in day_schedule:
                    self.scheduler.every().wednesday.at(class_schedule[0]).do(
                        func(class_schedule[1])
                    )

            elif day == "4":  # Thursday
                for class_schedule in day_schedule:
                    self.scheduler.every().thursday.at(class_schedule[0]).do(
                        func(class_schedule[1])
                    )

            elif day == "5":  # Friday
                for class_schedule in day_schedule:
                    self.scheduler.every().friday.at(class_schedule[0]).do(
                        func(class_schedule[1])
                    )

            elif day == "6":  # Saturday
                for class_schedule in day_schedule:
                    self.scheduler.every().saturday.at(class_schedule[0]).do(
                        func(class_schedule[1])
                    )

            elif day == "7":  # Sunday
                for class_schedule in day_schedule:
                    self.scheduler.every().sunday.at(class_schedule[0]).do(
                        func(class_schedule[1])
                    )

            else:
                raise ValueError(
                    "Invalid day number: {}. Must be within 1-7 (Monday-Sunday) range".format(
                        day
                    )
                )
