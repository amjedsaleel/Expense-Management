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

    path('verification/<uidb64>/<token>', views.VerificationView.as_view(), name='verification'),

    # API
    path('validate-username', csrf_exempt(views.UsernameValidationView.as_view()),
         name='validate-username'),
    path('validate-email', csrf_exempt(views.EmailValidationView.as_view()),
         name='validate-email'),

]
