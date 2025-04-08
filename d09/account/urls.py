from django.urls import path

from django.http import HttpResponse 
from . import views

app_name = 'account'

urlpatterns = [
	# path('account/', lambda request: HttpResponse('HELLo'), name='account'),
	path('', views.AccountView.as_view(), name='login'),
	path('logout/', views.LogoutView.as_view(), name='logout'),
	path('register/', views.RegisterView.as_view(), name='register'),
]
