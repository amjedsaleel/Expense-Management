# Django
from django.urls import path

# local Django
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expenses', views.add_expense, name='add-expense')
]
