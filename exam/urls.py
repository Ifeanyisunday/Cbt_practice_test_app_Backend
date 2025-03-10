from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import QuestionViewSet


urlpatterns = [
    path('questions/<int:amount>/<str:category>/', QuestionViewSet.as_view({'get': 'list_with_params'}), name='questions'),
    path('questions/get_questions/', QuestionViewSet.as_view({'get': 'get_questions'}), name='get_questions'),
    path('questions/submit_answers/', QuestionViewSet.as_view({'post': 'submit_answers'}), name='submit_answers'),
]

# create_user = http://127.0.0.1:8000/auth/users/

# login_user = http://127.0.0.1:8000/auth/jwt/create/

# refresh_token = http://127.0.0.1:8000/auth/jwt/refresh/

