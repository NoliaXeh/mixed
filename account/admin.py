from django.contrib import admin

from .models import Account, Relation, Alter, Front, System
# Register your models here.

admin.site.register([Account, Relation, Alter, Front, System])