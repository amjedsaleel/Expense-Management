# Django
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

# Local django
from . import views

app_name = 'auth'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),

    # Ajax requests
    path('validate-username', csrf_exempt(views.UsernameValidationView.as_view()),
         name='validate-username')
]
