from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

from .models import Account

class IndexView(generic.ListView):
    def get_queryset(self):
        return Account.objects.all()
        