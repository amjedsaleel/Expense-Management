# Standard library
import json

# Django
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User

# Create your views here.


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'User name only contains alphanumeric characters'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use, chose another one'}, status=409)
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')