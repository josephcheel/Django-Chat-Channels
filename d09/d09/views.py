from django.urls import path
from django.shortcuts import redirect

def redirect_home(request):
	return redirect('account:login')