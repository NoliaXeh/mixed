from typing import Callable
from django.db import models
from django.db.models import CharField, ForeignKey, IntegerField, CASCADE

from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL
from django.db.models.fields import DateTimeField, TextField
from django.db.models.fields.json import JSONField

# Create your models here.

def auto_str(cls):
    setattr(cls, "__str__", lambda self: f"{self.name}")
    setattr(cls, "__repr__", lambda self: f"<{type(self).__name__}: {str(self)}>")
    return cls

class Account(models.Model):
    display_name    = CharField     (max_length=64)
    user            = ForeignKey    (User, on_delete=CASCADE)
    profile_picture = CharField     (max_length=1024, default='https://i.ibb.co/DM0RM4f/default.png')
    __str__=lambda self: f"{self.display_name}"

@auto_str
class System(models.Model):
    name            = CharField     (max_length=64)
    account         = ForeignKey    (Account, on_delete=CASCADE)

@auto_str
class Alter(models.Model):
    system          = ForeignKey    (System, on_delete=CASCADE)
    name            = CharField     (max_length=64)
    age             = IntegerField  ()
    profile_picture = CharField     (max_length=1024, default='https://i.ibb.co/DM0RM4f/default.png')

@auto_str
class ChatRoom(models.Model):
    name            = CharField     (max_length=128)

class ChatRoomMembers(models.Model):
    chatroom        = ForeignKey    (ChatRoom, on_delete=CASCADE, unique=False)
    account         = ForeignKey    (Account, on_delete=CASCADE, unique=False)

class People(models.Model):
    account         = ForeignKey    (Account, on_delete=CASCADE)
    alter           = ForeignKey    (Alter, on_delete=CASCADE, null=True)
    __str__=lambda self:f"{self.account} ({self.alter})"

class Message(models.Model):
    body            = TextField     ()
    chatroom        = ForeignKey    (ChatRoom, on_delete=CASCADE)
    author          = ForeignKey    (People, on_delete=SET_NULL, null=True)
    created_at      = DateTimeField (auto_now_add=True)
    updated_at      = DateTimeField (auto_now=True)
    __str__=lambda self:f"{self.chatroom}: {self.body}"




