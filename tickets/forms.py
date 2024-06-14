from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import HardwareTicket, SoftwareTicket, Ticket


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    firstname = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'email', 'firstname', 'lastname', 'password1', 'password2']


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['estTicket', 'estAtendimento']


class HardwareTicketForm(TicketForm):
    class Meta(TicketForm.Meta):
        model = HardwareTicket
        fields = TicketForm.Meta.fields + ['equipamento', 'avaria']


class SoftwareTicketForm(TicketForm):
    class Meta(TicketForm.Meta):
        model = SoftwareTicket
        fields = TicketForm.Meta.fields + ['software', 'descNecessidade']


class HardwareTicketEditForm(forms.ModelForm):
    class Meta:
        model = HardwareTicket
        fields = ['estTicket', 'estAtendimento', 'descRep', 'pecas']


class SoftwareTicketEditForm(forms.ModelForm):
    class Meta:
        model = SoftwareTicket
        fields = ['estTicket', 'estAtendimento', 'descInt']
