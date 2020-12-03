# Django
from django.urls import path

# Local Django
from . import views

app_name = 'user-preferences'

urlpatterns = [
    path('', views.index, name='currency')
]