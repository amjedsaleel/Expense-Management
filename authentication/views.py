# Standard library
import json

# third-party
from validate_email import validate_email

# Django
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage

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


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Invalid mail'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry mail in use, chose another one'}, status=409)
        return JsonResponse({'email_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        context = {'filed_values': request.POST}

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 5:
                    messages.error(request, 'Password is too short. Choose password more than 6 characters')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                email_subject = 'Activate account'
                email_body = 'Test purpose, amjed saleel'
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreplay@gmail.com',
                    [email],
                    reply_to=['another@example.com'],
                    headers={'Message-ID': 'foo'},
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account successfully cretaed')
        return render(request, 'authentication/register.html')
