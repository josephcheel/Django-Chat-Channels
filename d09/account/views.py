from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.views.generic import CreateView

from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy
# Create your views here.

class AccountView(LoginView):
	template_name = 'account.html'
	success_url = '/account'

class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'register.html'
    
    success_url = '/account'  # Redirect to login page after registration

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     # You can add any additional logic here if needed
    #     return response
