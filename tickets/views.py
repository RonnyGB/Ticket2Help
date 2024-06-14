# views.py
from django.contrib import messages
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, ExpressionWrapper
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .ticket_helper import *
from .forms import RegisterForm, HardwareTicketForm, SoftwareTicketForm, HardwareTicketEditForm, SoftwareTicketEditForm
from django.http import Http404
from .forms import RegisterForm, HardwareTicketForm, SoftwareTicketForm, TicketForm
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from .models import Ticket
import pandas as pd


def index(request):
    return render(request, 'tickets/index.html')


@login_required
def new_ticket(request):
    hardware_form = HardwareTicketForm()
    software_form = SoftwareTicketForm()
    form = None
    ticket_type = None

    if request.method == 'POST':
        if 'ticket_type' in request.POST:
            ticket_type = request.POST['ticket_type']
            if ticket_type == 'hardware':
                form = HardwareTicketForm()
            elif ticket_type == 'software':
                form = SoftwareTicketForm()
        else:
            ticket_type = request.POST.get('tipo')
            if ticket_type == 'Hardware':
                form = HardwareTicketForm(request.POST)
                if form.is_valid():
                    equipamento = form.cleaned_data['equipamento']
                    avaria = form.cleaned_data['avaria']
                    ticket = HardwareTicket(idColaborador=request.user, estTicket='porAtender', estAtendimento='',
                                            equipamento=equipamento, avaria=avaria, tipo=request.POST.get('tipo'))
                    ticket.save()
                    return redirect('home')
            elif ticket_type == 'Software':
                form = SoftwareTicketForm(request.POST)
                if form.is_valid():
                    software = form.cleaned_data['software']
                    descNecessidade = form.cleaned_data['descNecessidade']
                    ticket = SoftwareTicket(idColaborador=request.user, estTicket='porAtender', estAtendimento='',
                                            software=software, descNecessidade=descNecessidade,
                                            tipo=request.POST.get('tipo'))
                    ticket.save()
                    return redirect('home')

    return render(
        request,
        'home/client/new_ticket.html',
        {
            'hardware_form': hardware_form,
            'software_form': software_form,
            'form': form,
            'ticket_type': ticket_type,
        }
    )


@login_required
def list_tickets(request):
    ticket_type = request.GET.get('type', 'all')
    tickets = []

    if ticket_type == 'hardware':
        tickets = HardwareTicket.objects.all()
    elif ticket_type == 'software':
        tickets = SoftwareTicket.objects.all()
    else:
        hardware_tickets = HardwareTicket.objects.all()
        software_tickets = SoftwareTicket.objects.all()
        tickets = list(hardware_tickets) + list(software_tickets)
        tickets.sort(key=lambda x: x.dtCriacao, reverse=True)  # Sort by creation date

    return render(request, 'home/client/list_tickets.html', {'tickets': tickets, 'ticket_type': ticket_type})


@login_required
def ticket_details(request, ticket_id):
    user = request.user
    try:
        ticket = HardwareTicket.objects.get(id=ticket_id)
        ticket_type = 'hardware'
    except HardwareTicket.DoesNotExist:
        try:
            ticket = SoftwareTicket.objects.get(id=ticket_id)
            ticket_type = 'software'
        except SoftwareTicket.DoesNotExist:
            raise Http404("Ticket does not exist")  # or render your custom 404 page

    if user.is_staff or user.has_perm('app_name.permission_codename'):
        return render(request, 'home/technic/ticket_details.html', {'ticket': ticket, 'ticket_type': ticket_type})
    else:
        return render(request, 'home/client/ticket_details.html', {'ticket': ticket, 'ticket_type': ticket_type})


@login_required
def manage_tickets(request):
    ticket_type = request.GET.get('type', 'all')
    if ticket_type == 'hardware':
        tickets = HardwareTicket.objects.all()
    elif ticket_type == 'software':
        tickets = SoftwareTicket.objects.all()
    else:
        hardware_tickets = HardwareTicket.objects.all()
        software_tickets = SoftwareTicket.objects.all()
        tickets = list(hardware_tickets) + list(software_tickets)
        tickets.sort(key=lambda x: x.dtCriacao, reverse=True)  # Sort by creation date

    return render(request, 'home/technic/manage_tickets.html', {'tickets': tickets, 'ticket_type': ticket_type})


@login_required
def edit_ticket(request, ticket_id):
    try:
        ticket = get_object_or_404(HardwareTicket, id=ticket_id)
        ticket_type = 'hardware'
        form_class = HardwareTicketEditForm
    except HardwareTicket.DoesNotExist:
        try:
            ticket = get_object_or_404(SoftwareTicket, id=ticket_id)
            ticket_type = 'software'
            form_class = SoftwareTicketEditForm
        except SoftwareTicket.DoesNotExist:
            return render(request, '404.html')  # or custom error handling

    # Check if the ticket's estAtendimento is 'resolvido'
    if ticket.estAtendimento == 'resolvido':
        messages.error(request, 'You cannot edit a resolved ticket.')
        return redirect('manage_tickets')  # or redirect to another appropriate page

    if request.method == 'POST':
        form = form_class(request.POST, instance=ticket)
        if form.is_valid():
            ticket.colaboradorAlt = request.user.username  # Update the colaboradorAlt field
            form.save()
            return redirect('manage_tickets')
    else:
        form = form_class(instance=ticket)

    return render(request, 'home/technic/edit_ticket.html', {'form': form, 'ticket_type': ticket_type})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            password = form.cleaned_data.get('password1')
            User.objects.create_user(username=username, email=email, password=password, first_name=firstname,
                                     last_name=lastname)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def home(request):
    user = request.user
    if user.is_staff or user.has_perm('app_name.permission_codename'):
        return render(request, 'home/technic.html')
    else:
        return render(request, 'home/client.html')


def tickets_atendidos(request):
    # Lógica para calcular os dados e gerar o gráfico de Tickets Atendidos
    # Exemplo básico:
    data_inicio = '2024-01-01'
    data_fim = '2024-06-30'

    tickets_atendidos = Ticket.objects.filter(
        dtCriacao__range=[data_inicio, data_fim],
        estAtendimento='Atendido'
    ).count()

    total_tickets = Ticket.objects.filter(
        dtCriacao__range=[data_inicio, data_fim]
    ).count()

    if total_tickets > 0:
        percentual_atendidos = (tickets_atendidos / total_tickets) * 100
    else:
        percentual_atendidos = 0

    # Criação do gráfico
    labels = ['Atendidos', 'Não Atendidos']
    sizes = [percentual_atendidos, 100 - percentual_atendidos]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    # Convertendo o gráfico para uma imagem base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    grafico_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()

    context = {'grafico_data': grafico_data}
    return render(request, 'home/technic/gen_report.html', context)


def tickets_resolvidos(request):
    # Lógica para calcular os dados e gerar o gráfico de Tickets Resolvidos
    tickets_resolvidos = Ticket.objects.filter(estTicket='Resolvido').count()
    total_tickets = Ticket.objects.count()

    if total_tickets > 0:
        percentual_resolvidos = (tickets_resolvidos / total_tickets) * 100
    else:
        percentual_resolvidos = 0

    # Criação do gráfico
    labels = ['Resolvidos', 'Não Resolvidos']
    sizes = [percentual_resolvidos, 100 - percentual_resolvidos]

    fig, ax = plt.subplots()
    ax.bar(labels, sizes, color=['green', 'red'])
    ax.set_ylabel('Percentual (%)')

    # Convertendo o gráfico para uma imagem base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    grafico_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()

    context = {'grafico_data': grafico_data}
    return render(request, 'home/technic/gen_report2.html', context)


def media_tempo_atendimento(request):
    tickets = Ticket.objects.all()

    total_tickets = 0
    total_tempo_atendimento = timedelta()

    for ticket in tickets:
        if ticket.dtCriacao and ticket.dtUltimaAlt:
            tempo_atendimento = ticket.dtUltimaAlt - ticket.dtCriacao
            total_tempo_atendimento += tempo_atendimento
            total_tickets += 1

    # Calculando a média de tempo de atendimento em minutos
    if total_tickets > 0:
        media_tempo_atendimento = total_tempo_atendimento.total_seconds() / 60 / total_tickets
    else:
        media_tempo_atendimento = 0

    context = {
        'media_tempo_atendimento': media_tempo_atendimento,
        # Outros dados que você deseja passar para o template
    }

    return render(request, 'home/technic/gen_report3.html', context)