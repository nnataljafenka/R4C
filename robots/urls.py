from django.urls import path

from . import views

app_name = 'create_robots'
urlpatterns = [
    path('create_robot/', views.RobotCreateView.as_view(), name='create_robot'),
    path('report/', views.RobotReportView.as_view(), name='robot_report'),
    path('download_report/', views.RobotReportView.download_report, name='download_report'),
]
