from typing import Callable
from django.db import models
from django.db.models import CharField, ForeignKey, IntegerField, CASCADE

from django.contrib.auth.models import User
from django.db.models.fields import TextField
from django.db.models.fields.json import JSONField

# Create your models here.

def auto_str(cls):
    setattr(cls, "__str__", lambda self: f"{self.name}")
    setattr(cls, "__repr__", lambda self: f"<{type(self).__name__}: {str(self)}>")
    return cls

@auto_str
class Account(models.Model):
    display_name    = CharField     (max_length=64)
    user            = ForeignKey    (User, on_delete=CASCADE)

@auto_str
class System(models.Model):
    name            = CharField     (max_length=64)
    account         = ForeignKey    (Account, on_delete=CASCADE)

@auto_str
class Alter(models.Model):
    system          = ForeignKey    (System, on_delete=CASCADE)
    name            = CharField     (max_length=64)
    age             = IntegerField  ()

@auto_str
class ChatRoom(models.Model):
    name            = CharField     (max_length=128)

class ChatRoomMembers(models.Model):
    chatroom        = ForeignKey    (ChatRoom, on_delete=CASCADE)
    account         = ForeignKey    (Account, on_delete=CASCADE)

class Message(models.Model):
    body            = TextField     ()
    chatroom        = ForeignKey    (ChatRoom, on_delete=CASCADE)
    author          = JSONField     () # list of authors

    __str__=lambda self: f"{self.chatroom}: {body}"

# class MessageAuthors(models.Model):
#     message         = ForeignKey    (Message, on_delete=CASCADE)
#     account         = ForeignKey    (Account, on_delete=CASCADE, null=True)
#     system          = ForeignKey    (System , on_delete=CASCADE, null=True)
#     alter           = ForeignKey    (Alter  , on_delete=CASCADE, null=True)




