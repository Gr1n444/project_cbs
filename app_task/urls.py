from django.urls import path
from app_task.views import *


urlpatterns = [
    path('tasks', Tasks, name='ctfTasks'),
    path('task/<int:task_id>/', view_Task, name='view_ctfTask'),
    path('events', Events, name='ctfEvents'),
    path('event/<int:task_id>/', view_Event, name='view_ctfEvent'),
]