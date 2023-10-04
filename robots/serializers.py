from django.core.exceptions import ValidationError
from .models import Robot
import datetime
import json


class RobotSerializer:
    def __init__(self, data):
        self.data = data
        self.model = data["model"]
        self.version = data["version"]
        self.serial = self.model + '-' + self.version
        self.created = datetime.datetime.strptime(data["created"], "%Y-%m-%d %H:%M:%S")

    def is_valid(self):
        if not (isinstance(self.serial, str) and len(self.serial) <= 5):
            return False
        if not (isinstance(self.model, str) and len(self.model) == 2):
            return False
        if not (isinstance(self.version, str) and len(self.version) == 2):
            return False
        return True

    def save(self):
        robot = Robot(serial=self.serial, model=self.model, version=self.version, created=self.created)
        robot.save()
