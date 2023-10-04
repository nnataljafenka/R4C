from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from .models import Robot
from .serializers import RobotSerializer
import json
import datetime


# Create your views here.
class RobotCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            serializer = RobotSerializer(data)
            if serializer.is_valid():
                # Проверка на наличие модели
                existing_robot = Robot.objects.filter(serial=serializer.serial).first()
                if existing_robot:
                    return JsonResponse({'message': 'Robot have already existed'}, status=400)

                serializer.save()

                response_data = {
                    'message': 'Robot created successfully!',
                    'robot_data': {
                        'serial': serializer.serial,
                        'model': serializer.model,
                        'version': serializer.version,
                        'created': serializer.created.strftime("%Y-%m-%d %H:%M:%S")
                    }
                }
                return JsonResponse(response_data, status=201)
            else:
                return JsonResponse({'error': 'Invalid JSON format or data. Valid format: {"model":"model_name","version":"version_name","created":"date"}, format date:"%Y-%m-%d %H:%M:%S"'}, status=400)
        except (json.JSONDecodeError, ValueError, TypeError, KeyError, OverflowError):
            return HttpResponseBadRequest('Invalid JSON data')
