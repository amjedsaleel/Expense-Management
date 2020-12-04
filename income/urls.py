# Django
from django.views.decorators.csrf import csrf_exempt
from django.urls import path

# Local Django


from . import views

app_name = 'income'

urlpatterns = [
    path('', views.index, name='income'),
    path('add-income/', views.AddIncomeView.as_view(), name='add-income'),
    path('edit-income/<int:pk>', views.edit_income, name='edit-income'),
    path('income-delete/<int:id>', views.income_delete, name='income-delete'),

    # API
    path('search-income', csrf_exempt(views.income_search), name='search-income')
]
