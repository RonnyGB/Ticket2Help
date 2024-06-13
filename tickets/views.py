# views.py
from django.shortcuts import render
from .ticket_helper import *
from django.http import HttpResponse


def index(request):
    return render(request, 'tickets/index.html')


def list_tickets(request):
    tickets = get_tickets(request)
    return render(request, 'myapp/list_tickets.html', {'tickets': tickets})