from django.urls import path
from app_test.views import *

app_name = 'app_test'

urlpatterns = [
    path('tests/', tests, name='tests'),
    path('<int:test_id>/', display_test, name='display_test'),
    path('<int:test_id>/questions/<int:question_id>', display_question, name='display_question'),
    path('<int:test_id>/questions/<int:question_id>/grade/', grade_question, name='grade_question'),
    path('results/<int:test_id>/', test_results, name='test_results'), 
]