from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages import success, error, info
from django.views import View
from django.contrib.auth import get_user_model, login

User = get_user_model()

# Create your views here.

class MyLoginView(LoginView):
    template_name = "login.html"

class MyLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        success(request, "Logged out")
        return redirect("login")

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            info(request, "You are already logged in.")
            return redirect('dashboard')
        return render(request, 'register.html')
    def post(self, request, *args, **kwargs):
        provided_username = request.POST['username']
        provided_password = request.POST['password']
        if User.objects.filter(username=provided_username).count():
            error(request, "Different user with the same username already exists!")
            return redirect(self.request.path_info)
        user = User.objects.create_user(username=provided_username, password=provided_password)
        login(request, user)
        success(request, "Registered account successfully!")
        return redirect('dashboard')