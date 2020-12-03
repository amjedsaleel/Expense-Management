from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View

# Create your views here.

# Local Django


from . models import UserIncome, Source


def index(request):
    income = UserIncome.objects.filter(owner=request.user)

    context = {
        'income': income
    }

    return render(request, 'income/index.html', context)


@method_decorator(login_required(login_url='auth:login'), name='dispatch')
class AddIncomeView(View):
    template_name = 'income/add-income.html'

    def get(self, request):
        return render(request, self.template_name, context={'categories': self.categories})


