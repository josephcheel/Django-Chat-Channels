from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
	chat_room = models.ForeignKey('chatRoom', on_delete=models.CASCADE)
	sender = models.ForeignKey(User, on_delete=models.CASCADE)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.sender

class chatRoom(models.Model):
	name = models.CharField(
		max_length=100,
		validators=[
			RegexValidator(
				regex=r'^[a-zA-Z0-9._-]+$',
				message='Name must be a valid unicode string containing only ASCII alphanumerics, hyphens, underscores, or periods.'
			)
		]
	)
	description = models.TextField(max_length=200, blank=True)
	sub_description = models.TextField(max_length=100, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	last_three_messages = models.ManyToManyField(Message, blank=True)
	def __str__(self):
		return self.name
