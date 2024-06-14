from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import HardwareTicket, SoftwareTicket, Ticket


class RegisterForm(UserCreationForm):
    """
    Formulário de registro de usuário que inclui campos adicionais como email, 
    primeiro nome e sobrenome.
    
    Campos:
        - username: Nome de usuário
        - email: Email do usuário
        - firstname: Primeiro nome do usuário
        - lastname: Sobrenome do usuário
        - password1: Senha
        - password2: Confirmação da senha
    """
    email = forms.EmailField(required=True)
    firstname = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'email', 'firstname', 'lastname', 'password1', 'password2']


class TicketForm(forms.ModelForm):
    """
    Formulário base para tickets. Inclui os campos básicos de estado do ticket 
    e estado do atendimento.

    Campos:
        - estTicket: Estado do ticket
        - estAtendimento: Estado do atendimento
    """
    class Meta:
        model = Ticket
        fields = ['estTicket', 'estAtendimento']


class HardwareTicketForm(TicketForm):
    """
    Formulário específico para tickets de hardware. Herda os campos do 
    TicketForm e adiciona campos específicos de hardware.

    Campos:
        - equipamento: Equipamento relacionado ao ticket
        - avaria: Descrição da avaria do equipamento
    """
    class Meta(TicketForm.Meta):
        model = HardwareTicket
        fields = TicketForm.Meta.fields + ['equipamento', 'avaria']


class SoftwareTicketForm(TicketForm):
    """
    Formulário específico para tickets de software. Herda os campos do 
    TicketForm e adiciona campos específicos de software.

    Campos:
        - software: Software relacionado ao ticket
        - descNecessidade: Descrição da necessidade do software
    """
    class Meta(TicketForm.Meta):
        model = SoftwareTicket
        fields = TicketForm.Meta.fields + ['software', 'descNecessidade']


class HardwareTicketEditForm(forms.ModelForm):
    """
    Formulário para edição de tickets de hardware. Inclui campos adicionais 
    para detalhes de reparo e peças utilizadas.

    Campos:
        - estTicket: Estado do ticket
        - estAtendimento: Estado do atendimento
        - descRep: Descrição do reparo realizado
        - pecas: Peças utilizadas no reparo
    """
    class Meta:
        model = HardwareTicket
        fields = ['estTicket', 'estAtendimento', 'descRep', 'pecas']


class SoftwareTicketEditForm(forms.ModelForm):
    """
    Formulário para edição de tickets de software. Inclui campos adicionais 
    para descrição da intervenção.

    Campos:
        - estTicket: Estado do ticket
        - estAtendimento: Estado do atendimento
        - descInt: Descrição da intervenção realizada
    """
    class Meta:
        model = SoftwareTicket
        fields = ['estTicket', 'estAtendimento', 'descInt']
