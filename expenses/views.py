# Standard library
import json

# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.http import JsonResponse

# Local django
import userpreferences
from .models import Expense, Category
from userpreferences.models import UserPreference


# Create your views here.

def expense_search(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str,
            owner=request.user) | Expense.objects.filter(category__icontains=search_str, owner=request.user)

        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='auth:login')
def index(request):
    expenses = Expense.objects.filter(owner=request.user).order_by('-date')
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'expenses/index.html', context)


@method_decorator(login_required(login_url='auth:login'), name='dispatch')
class AddExpenseView(View):
    template_name = 'expenses/add_expense.html'
    categories = Category.objects.all()

    def get(self, request):
        return render(request, self.template_name, context={'categories': self.categories})

    def post(self, request):
        amount = request.POST['amount']
        context = {
            'values': request.POST,
            'categories': self.categories
        }

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, self.template_name, context)

        Expense.objects.create(
            amount=request.POST['amount'],
            date=request.POST['date'],
            description=request.POST['description'],
            category=request.POST['category'],
            owner=request.user
        )
        messages.success(request, 'Expense saved successfully')
        return redirect('expenses:expenses')


def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()

    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }

    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.date = request.POST['date']
        expense.category = request.POST['category']
        expense.description = request.POST['description']

        expense.save()
        messages.success(request, 'Expense is updated')

        return redirect('expenses:expenses')


def expense_delete(request, id):
    expense = Expense.objects.get(pk=id).delete()
    messages.success(request, 'Expense is deleted')
    return redirect('expenses:expenses')
