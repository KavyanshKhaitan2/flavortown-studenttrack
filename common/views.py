from django.shortcuts import render
from django.contrib.auth.views import LoginView

# Create your views here.

class MyLoginView(LoginView):
    template_name = "login.html"