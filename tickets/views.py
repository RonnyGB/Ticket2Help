# views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .ticket_helper import *
from .forms import RegisterForm, HardwareTicketForm, SoftwareTicketForm, TicketForm
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from .models import Ticket


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
                    ticket = HardwareTicket(idColaborador=request.user, estTicket='porAtender', estAtendimento='Aberto', equipamento=equipamento, avaria=avaria, tipo=request.POST.get('tipo'))
                    ticket.save()
                    return redirect('home')
            elif ticket_type == 'Software':
                form = SoftwareTicketForm(request.POST)
                if form.is_valid():
                    software = form.cleaned_data['software']
                    descNecessidade = form.cleaned_data['descNecessidade']
                    ticket = SoftwareTicket(idColaborador=request.user, estTicket='porAtender', estAtendimento='Aberto', software=software, descNecessidade=descNecessidade, tipo=request.POST.get('tipo'))
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
def list_tickets(request, tipo):
    tickets = get_tickets(op=tipo)
    print(tickets)
    user = request.user
    if user.is_staff or user.has_perm('app_name.permission_codename'):
        return render(request, 'home/technic/list_tickets.html', {'tickets': tickets})
    else:
        return render(request, 'home/client/list_tickets.html', {'tickets': tickets})


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


def tickets_atendidos_por_data(request):
    # Exemplo de intervalo de datas (substitua com seus dados reais)
    data_inicio = '2024-01-01'
    data_fim = '2024-06-30'

    # Consulta para obter o número de tickets atendidos no intervalo de datas
    tickets_atendidos = Ticket.objects.filter(
        dtCriacao__range=[data_inicio, data_fim],
        estAtendimento='Atendido'
    ).count()

    # Consulta para obter o número total de tickets no intervalo de datas
    total_tickets = Ticket.objects.filter(
        dtCriacao__range=[data_inicio, data_fim]
    ).count()

    # Calcular percentual de tickets atendidos
    if total_tickets > 0:
        percentual_atendidos = (tickets_atendidos / total_tickets) * 100
    else:
        percentual_atendidos = 0

    # Criar gráfico de pizza
    labels = ['Atendidos', 'Não Atendidos']
    sizes = [percentual_atendidos, 100 - percentual_atendidos]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Salvar gráfico como imagem base64 para exibir na template
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    grafico_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()

    context = {'grafico_data': grafico_data}
    return render(request, 'home/technic/gen_report.html', context)