# Standard library
import os
import json

# Django
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages

# Local Django
from .models import UserPreference


# Create your views here.


def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            currency_data.append({'name': key, 'value': value})

    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preference = None

    if exists:
        user_preference = UserPreference.objects.get(user=request.user)

    if request.method == "GET":
        context = {
            'currencies': currency_data,
            'user_preference': user_preference
        }

        return render(request, 'preferences/index.html', context)
    else:
        currency = request.POST['currency']

        if exists:
            user_preference.currency = currency
            user_preference.save()
            messages.success(request, 'Changes saved')
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
        return render(request, 'preferences/index.html',
                      {'currencies': currency_data, 'user_preference': user_preference})
