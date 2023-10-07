from django.urls import path

from . import views

app_name = 'create_robots'
urlpatterns = [
    path('create_robot/', views.RobotCreateView.as_view(), name='create_robots'),
]
