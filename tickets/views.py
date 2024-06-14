# views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .ticket_helper import *
from .forms import RegisterForm, HardwareTicketForm, SoftwareTicketForm, HardwareTicketEditForm, SoftwareTicketEditForm
from django.http import Http404


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
