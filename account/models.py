from django.db import models
from django.contrib.auth.models import User
import datetime



class Account(models.Model):
    user        = models.ForeignKey     (User, on_delete=models.CASCADE)
    color       = models.CharField      (max_length=6, default="0000FF") # hexcode for color
    birthday    = models.DateField      ()
    description = models.TextField      (default="", blank=True, null=True)
    avatar      = models.ImageField     (blank=True, null=True)
    pronouns    = models.CharField      (max_length=32, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.user.username} : {self.user.email}'

    def __repr__(self) -> str:
        return f'Account({str(self)})'


class System(models.Model):
    name        = models.CharField      (max_length=32)
    account     = models.ForeignKey     (Account, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f'{self.name} ({self.account.user if self.account else "NULL"})'

    def __repr__(self) -> str:
        return f'System({str(self)})'

class Relation(models.Model):
    FRIEND      = "FR"
    BLOCK       = "BL"
    REQUESTING  = "RE"
    JUST_CHAT   = "CH"

    RELATIONS   = [
        (FRIEND,        "Friend"),
        (BLOCK,         "Blocked"),
        (REQUESTING,    "Requesting"),
        (JUST_CHAT,     "Just Chatting"),
    ]

    left_user   = models.ForeignKey     (Account, on_delete=models.DO_NOTHING, related_name="left_user")
    right_user  = models.ForeignKey     (Account, on_delete=models.DO_NOTHING, related_name="right_user")
    relation    = models.CharField      (max_length=2, choices=RELATIONS, default=JUST_CHAT)

    def __str__(self) -> str:
        relations = {id: value for id,value in Relation.RELATIONS}
        return f'{self.left_user.username} <-> {self.right_user.username} : {relations[self.relation]}'

    def __repr__(self) -> str:
        return f'Relation({str(self)})'

class Alter(models.Model):
    name        = models.CharField      (max_length=32)
    system      = models.ForeignKey     (System, on_delete=models.CASCADE)
    avatar      = models.ImageField     (blank=True, null=True)
    pronouns    = models.CharField      (max_length=32, blank=True, null=True)
    color       = models.CharField      (max_length=6, default="0000FF") # hexcode for color
    birthday    = models.DateField      (blank=True, null=True)
    description = models.TextField      (default="", blank=True, null=True)
    roles       = models.CharField      (max_length=32,blank=True, null=True)
    is_fragment = models.BooleanField   (default=False)
    groups      = models.CharField      (max_length=512, default="")

    def __str__(self) -> str:
        return f'{self.system.name} : {self.name}'

    def __repr__(self) -> str:
        return f'Alter({str(self)})'

class Front(models.Model):
    FRONT       = "FR"
    COCONSCIUOS = "CO"
    BLEND       = "BL"
    FRONT_TYPE  = [
        (FRONT,         "Fronting"),
        (COCONSCIUOS,   "Co-Conscious"),
        (BLEND,         "Blent"),
    ]
    system      = models.ForeignKey     (System, on_delete=models.CASCADE)
    alter       = models.ForeignKey     (Alter,  on_delete=models.CASCADE)
    is_main     = models.BooleanField   (default=False)
    age         = models.IntegerField   (blank=True, null=True)
    start       = models.DateTimeField  (default=datetime.datetime.now)
    end         = models.DateTimeField  (blank=True, null=True)
    front_type  = models.CharField      (max_length=2, choices=FRONT_TYPE)