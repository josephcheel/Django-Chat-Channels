from django.urls import path

from . import views

from django.http import HttpResponse

app_name = 'chat'

urlpatterns = [
	path('', views.chat_view, name='index'),
	path('<str:room_name>/', views.chat_view, name='chat'),
]