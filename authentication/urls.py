# Django
from django.urls import path

# Local django
from . import views

app_name = 'auth'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
]
