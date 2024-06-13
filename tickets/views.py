# views.py
from django.shortcuts import render
from .ticket_helper import *
from django.http import HttpResponse


def index(request):
    return render(request, 'tickets/index.html')


def list_tickets(request, tipo=0):
    tickets = get_tickets(op=tipo)
    return render(request, 'myapp/list_tickets.js', {'tickets': tickets})