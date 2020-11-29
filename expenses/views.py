# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

# Local django
from . models import Expense, Category

# Create your views here.


@login_required(login_url='auth:login')
def index(request):
    return render(request, 'expenses/index.html')


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


