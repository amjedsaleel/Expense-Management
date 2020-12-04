# Standard library
import json

# Django
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import JsonResponse

# Local Django
from .models import UserIncome, Source
from userpreferences.models import UserPreference

# Create your views here.


def income_search(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = UserIncome.objects.filter(amount__istartswith=search_str,
                                             owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str,
            owner=request.user) | UserIncome.objects.filter(source__icontains=search_str, owner=request.user)

        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='auth:login')
def index(request):
    incomes = UserIncome.objects.filter(owner=request.user)
    currency = UserPreference.objects.get(user=request.user).currency

    paginator = Paginator(incomes, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {
        'incomes': incomes,
        'currency': currency,
        'page_obj': page_obj,
    }

    return render(request, 'income/index.html', context)


@method_decorator(login_required(login_url='auth:login'), name='dispatch')
class AddIncomeView(View):
    template_name = 'income/add-income.html'
    source = Source.objects.all()

    def get(self, request):
        return render(request, self.template_name, context={'source': self.source})

    def post(self, request):
        amount = request.POST['amount']
        context = {
            'values': request.POST,
            'source': self.source
        }

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, self.template_name, context)

        UserIncome.objects.create(
            amount=request.POST['amount'],
            date=request.POST['date'],
            description=request.POST['description'],
            source=request.POST['source'],
            owner=request.user
        )
        messages.success(request, 'Income saved successfully')
        return redirect('income:income')


def edit_income(request, pk):
    income = UserIncome.objects.get(pk=pk)
    source = Source.objects.all()

    context = {
        'income': income,
        'values': income,
        'source': source
    }

    if request.method == 'GET':
        return render(request, 'income/edit-income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit-income.html', context)

        income.owner = request.user
        income.amount = amount
        income.date = request.POST['date']
        income.category = request.POST['source']
        income.description = request.POST['description']

        income.save()
        messages.success(request, 'Income is updated')

        return redirect('income:income')


def income_delete(request, id):
    user_income = UserIncome.objects.get(pk=id).delete()
    messages.success(request, 'Income is deleted')
    return redirect('income:income')
