from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from channels.exceptions import DenyConnection
from asgiref.sync import async_to_sync

import json

from .models import chatRoom, Message
connected_users = set()

class ChatConsumer(WebsocketConsumer):
	def send_left(self, event):
		username = event['username']

		# Send message to WebSocket
		self.send(text_data=json.dumps({
			'type': 'left',
			'username': username,
			'connected_users': list(connected_users)
		}))

	def send_joined(self, event):
		username = event['username']

		# Send message to WebSocket
		self.send(text_data=json.dumps({
			'type': 'joined',
			'username': username,
			'connected_users': list(connected_users)
		}))
	
	def connect(self):
		if not self.scope['user'].is_authenticated or isinstance(self.scope['user'], AnonymousUser) or self.scope['user'] is None:
			self.close()
			raise DenyConnection("You must be authenticated to connect.")
		

		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = self.room_name
		if self.room_name not in chatRoom.objects.values_list('name', flat=True):
			self.close(code=1)
			raise DenyConnection("Room does not exist.")

		self.username = self.scope['user'].username 
		connected_users.add(self.username)
        
		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)
		self.accept()

		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,
			{
				'type': 'send_joined',
				'username': self.scope["user"].username,
				'connected_users': list(connected_users)
			}
		)

	def disconnect(self, close_code):
		if close_code == 1:
			return
		username = self.scope["user"].username
		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,
			{
				'type': 'send_left',
				'username': username,
				'connected_users': list(connected_users)
			}
		)
		connected_users.remove(username)
		async_to_sync(self.channel_layer.group_discard)(
			self.room_group_name,
			self.channel_name
		)


	def receive(self, text_data=None):
		
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		
		username = self.scope["user"].username

		# Broadcast the message to the group
		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,
			{
				'type': 'chat_message',
				'message': message,
				'username': username
			}
		)

	def chat_message(self, event):
		message = event['message']
		username = event['username']


		if message.strip() == '':
			return
		
		try:
			room = chatRoom.objects.get(name=self.room_name)
		except chatRoom.DoesNotExist:
			return

		if room.last_three_messages.count() == 3:
			room.last_three_messages.order_by('created_at').first().delete()

		room.last_three_messages.add(Message.objects.create(
			chat_room=room,
			sender=self.scope["user"],
			message=message
		))


		# Send message to WebSocket
		self.send(text_data=json.dumps({
			'type': 'message',
			'message': message,
			'username': username
		}))

	
	

