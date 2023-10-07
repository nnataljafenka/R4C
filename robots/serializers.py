from django.core.exceptions import ValidationError
from .models import Robot
import datetime
import json
from django.http import HttpResponseBadRequest

class RobotSerializer:
    # class Meta:
    #     model = Robot
    #     fields = ("serial", "model", "version", "created")
    #     validators = [validate_alphanumeric]
    def validate_alphanumeric(self,value):
        if not value.isalnum():
            raise ValidationError(f'Значение {value} не верно. Только цифры и буквы разрешены.')

    def parse_json(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            self.model = data["model"]
            self.version = data["version"]
            self.serial = self.model + '-' + self.version
            self.created = datetime.datetime.strptime(data["created"], "%Y-%m-%d %H:%M:%S")
        except (json.JSONDecodeError, ValueError, TypeError, KeyError, OverflowError):
            return HttpResponseBadRequest('Invalid JSON data')

    def is_valid(self):
        if all(hasattr(self, attr) for attr in ["model", "version", "created"]):
            self.validate_alphanumeric(self.model)
            self.validate_alphanumeric(self.version)
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
