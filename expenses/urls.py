# Django
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

# local Django
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expenses', views.AddExpenseView.as_view(), name='add-expense'),
    path('edit-expense/<int:pk>', views.edit_expense, name='edit-expense'),
    path('expense-delete/<int:id>', views.expense_delete, name='expense-delete'),

    # API
    path('search-expense', csrf_exempt(views.expense_search), name='search-expense')
]
