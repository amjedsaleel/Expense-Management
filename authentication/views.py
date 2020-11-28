# Standard library
import json

# third-party
from validate_email import validate_email

# Django
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout

# Local Django
from . utils import account_activation_token

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

                # - path to view
                # - getting domain
                #  -relative url to activate account
                # - encode url
                # - token
                uid64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('auth:verification', kwargs={
                    'uidb64': uid64,
                    'token': account_activation_token.make_token(user)
                })

                activate_url = 'http://'+domain+link

                email_subject = 'Activate account'
                email_body = 'Hi '+user.username + 'Please use this link to verify your account\n' + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreplay@gmail.com',
                    [email],
                    reply_to=['another@example.com'],
                    headers={'Message-ID': 'foo'},
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account successfully created. Verification link mailed to your email')
        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):

        # try/except
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not account_activation_token.check_token(user, token):
                return redirect('auth:login'+'?message='+'User is already activated')

            if user.is_active:
                messages.success(user, 'Already activated. You can login now.')
                return redirect('auth:login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account is success fully activated')
            return redirect('auth:login')

        except Exception as ex:
            pass
        return redirect('auth:login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Welcome, ' + user.username + ' your are now logged in')
                    return redirect('expenses:expenses')
                else:
                    messages.error(request, 'Your account is not activate, please check your email.')
                    return render(request, 'authentication/login.html')
            else:
                messages.error(request, 'invalid credentials')
                return render(request, 'authentication/login.html')
        else:
            messages.error(request, 'Please fill username and password')
            return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('auth:login')
