from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import uuid


class Ticket(models.Model):
    ESTTICKET_OPT = [
        ('porAtender', 'Por Atender'),
        ('emAtendimento', 'Em Atendimento'),
        ('atendido', 'Atendido'),
    ]
    ESTATENDIMENTO_OPT = [
        ('aberto', 'Aberto'),
        ('resolvido', 'Resolvido'),
        ('naoResolvido', 'Não Resolvido'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dtCriacao = models.DateTimeField(auto_now_add=True)
    dtUltimaAlt = models.DateTimeField(auto_now=True)
    colaboradorAlt = models.CharField(max_length=100, null=True, blank=True)
    idColaborador = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    estTicket = models.CharField(max_length=50, default="porAtender", choices=ESTTICKET_OPT)
    estAtendimento = models.CharField(max_length=50, choices=ESTATENDIMENTO_OPT, null=True, blank=True,)
    tipo = models.CharField(max_length=50, null=True, blank=True)
    idColaborador = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.tipo} Ticket {self.id}'

    def printTicket(self):
        return f"ID: {self.id}\n" \
               f"Data de Criação: {self.dtCriacao}\n" \
               f"Data da Última Alteração: {self.dtUltimaAlt}\n" \
               f"Colaborador da Última Alteração: {self.colaboradorAlt}\n" \
               f"ID do Colaborador: {self.idColaborador}\n" \
               f"Estado do Ticket: {self.estTicket}\n" \
               f"Estado do Atendimento: {self.estAtendimento}\n" \
               f"Tipo de Ticket: {self.tipo}"


class HardwareTicket(Ticket):
    equipamento = models.CharField(max_length=100, null=True, blank=True)
    avaria = models.TextField(null=True, blank=True)
    descRep = models.TextField(null=True, blank=True)
    pecas = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Hardware Ticket {self.id}'

    def printTicket(self):
        return super().printTicket() + \
            f"\nEquipamento: {self.equipamento}\n" \
            f"Avaria: {self.avaria}\n" \
            f"Descrição da Reparação: {self.descRep}\n" \
            f"Peças: {self.pecas}"


class SoftwareTicket(Ticket):
    software = models.CharField(max_length=100, null=True, blank=True)
    descNecessidade = models.TextField(null=True, blank=True)
    descInt = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Software Ticket {self.id}'

    def printTicket(self):
        return super().printTicket() + \
            f"\nSoftware: {self.software}\n" \
            f"Descricao da Necessidade: {self.descNecessidade}\n" \
            f"Descrição de Intervençãp: {self.descInt}"
