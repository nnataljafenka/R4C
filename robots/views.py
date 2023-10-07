from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views import View
from django.views.generic import TemplateView
from .models import Robot
from .serializers import RobotSerializer
import json
import openpyxl
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter
import datetime


# Create your views here.
class RobotCreateView(View):
    def post(self, request):
        robot = RobotSerializer()
        robot.parse_json(request)
        if robot.is_valid():
            robot.save()
            response_data = {
                'message': 'Robot created successfully!',
                'robot_data': {
                    'serial': robot.serial,
                    'model': robot.model,
                    'version': robot.version,
                    'created': robot.created.strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({
                'error': 'Invalid JSON format or data. Valid format: {"model":"model_name","version":"version_name","created":"date"}, format date:"%Y-%m-%d %H:%M:%S"'},
                status=400)

