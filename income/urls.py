# Django
from django.urls import path

# Local Django
from . import views

app_name = 'income'

urlpatterns = [
    path('', views.index, name='income'),
    path('add-income/', views.AddIncomeView.as_view(), name='add-income')
]
