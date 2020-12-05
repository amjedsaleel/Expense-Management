# Django
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

# Local django
from . import views

app_name = 'auth'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('request-reset-link', views.RequestPasswordResetEmail.as_view(), name='request-reset-link'),

    path('verification/<uidb64>/<token>', views.VerificationView.as_view(), name='verification'),
    path('set-new-password/<uidb64>/<token>', views.CompletePasswordRestView.as_view, name='rest-user-password'),

    # API
    path('validate-username', csrf_exempt(views.UsernameValidationView.as_view()),
         name='validate-username'),
    path('validate-email', csrf_exempt(views.EmailValidationView.as_view()),
         name='validate-email'),
]
