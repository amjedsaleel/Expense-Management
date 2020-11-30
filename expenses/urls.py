# Django
from django.urls import path

# local Django
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expenses', views.AddExpenseView.as_view(), name='add-expense'),
    path('edit-expense/<int:id>', views.edit_expense, name='edit-expense'),
    path('expense-delete/<int:id>', views.expense_delete, name='expense-delete')
]
