from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import chatRoom
# Create your views here.

@login_required(login_url='/')
def chat_view(request, *args, **kwargs):
	room_name = kwargs.get('room_name')

	if room_name:
		try:
			chat_room = chatRoom.objects.get(name=room_name)
		except chatRoom.DoesNotExist:
			return redirect('chat:index')

		last_three_messages = chat_room.last_three_messages.all()
		return render(request, 'chat.html', {
			'chatRoom': chat_room,
			'messages': last_three_messages
		})

	else:
		return render(request, 'chatrooms_list.html', {
			'chatrooms': chatRoom.objects.all()
		})
