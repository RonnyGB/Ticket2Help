from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import uuid


class Ticket:
    def __init__(self, ):
        self._id = uuid.uuid4()
        self._dtCriacao = datetime.now()
        self.dtUltimaAlt = None
        self.ColaboradorAlt = None
        self.idColaborador = None
        self.estTicket = "porAtender"
        self.estAtendimento = "Aberto"
        self.Tipo = None


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def dtCriacao(self):
        return self._dtCriacao

    @dtCriacao.setter
    def dtCriacao(self, value):
        self._dtCriacao = value

    @property
    def idColaborador(self):
        return self._idColaborador

    @idColaborador.setter
    def idColaborador(self, value):
        self._idColaborador = value

    @property
    def ColaboradorAlt(self):
        return self._colaboradorAlt

    @ColaboradorAlt.setter
    def ColaboradorAlt(self, value):
        self._colaboradorAlt = value

    @property
    def estTicket(self):
        return self._estTicket

    @estTicket.setter
    def estTicket(self, value):
        self._estTicket = value

    @property
    def estAtendimento(self):
        return self._estAtendimento

    @estAtendimento.setter
    def estAtendimento(self, value):
        self._estAtendimento = value

    @property
    def dtUltimaAlt(self):
        return self._dtUltimaAlt

    @dtUltimaAlt.setter
    def dtUltimaAlt(self, value):
        self._dtUltimaAlt = value

    @property
    def Tipo(self):
        return self._tipo

    @Tipo.setter
    def Tipo(self, value):
        self._tipo = value

    def printTicket(self):
        return f"ID: {self._id}\n" \
               f"Data de Criação: {self._dtCriacao}\n" \
               f"Data da Última Alteração: {self.dtUltimaAlt}\n" \
               f"Colaborador da Última Alteração: {self.ColaboradorAlt}\n" \
               f"ID do Colaborador: {self.idColaborador}\n" \
               f"Estado do Ticket: {self.estTicket}\n" \
               f"Estado do Atendimento: {self.estAtendimento}\n" \
               f"Tipo de Ticket: {self.Tipo}"


class HardwareTicket(Ticket):
    def __init__(self, ):
        super().__init__()
        self._idHard = uuid.uuid4()
        self.Equipamento = None
        self.Avaria = None
        self.DescRep = None
        self.Pecas = None
        self.Tipo = "Hardware"
        self.ticketID = self.id


    @property
    def idHard(self):
        return self._idHard

    @idHard.setter
    def idHard(self, value):
        self._idHard = value

    @property
    def Equipamento(self):
        return self._equipamento

    @Equipamento.setter
    def Equipamento(self, value):
        self._equipamento = value

    @property
    def Avaria(self):
        return self._avaria

    @Avaria.setter
    def Avaria(self, value):
        self._avaria = value

    @property
    def DescRep(self):
        return self._descRep

    @DescRep.setter
    def DescRep(self, value):
        self._descRep = value

    @property
    def Pecas(self):
        return self._pecas

    @Pecas.setter
    def Pecas(self, value):
        self._pecas = value

    def printTicket(self):
        return super().printTicket() + \
           f"\nEquipamento: {self.Equipamento}\n"\
           f"Avaria: {self.Avaria}\n"\
           f"Descrição da Reparação: {self.DescRep}\n"\
           f"Peças: {self.Pecas}"


class SoftwareTicket(Ticket):
    def __init__(self, ):
        super().__init__()
        self._idSoft = uuid.uuid4()
        self.Software = None
        self.DescNecessidade = None
        self.DescInt = None
        self.Tipo = "Software"
        self.ticketID = self.id

    @property
    def idSoft(self):
        return self._idSoft

    @idSoft.setter
    def idSoft(self, value):
        self._idSoft = value
    @property
    def Software(self):
        return self._software

    @Software.setter
    def Software(self, value):
        self._software = value

    @property
    def DescNecessidade(self):
        return self._descNecessidade

    @DescNecessidade.setter
    def DescNecessidade(self, value):
        self._descNecessidade = value

    @property
    def DescInt(self):
        return self._descInt

    @DescInt.setter
    def DescInt(self, value):
        self._descInt = value

    def printTicket(self):
        return super().printTicket() + \
            f"\nSoftware: {self.Software}\n" \
            f"Descricao da Necessidade: {self.DescNecessidade}\n" \
            f"Descrição de Intervençãp: {self.DescInt}"


# class UserProfile(models.Model):
#     # Modelo para o perfil de utilizador
#     NIVEL_AUTORIZACAO = [
#         (1, 'Cliente'),
#         (2, 'Técnico'),
#     ]
#
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     autorizacao = models.IntegerField(choices=NIVEL_AUTORIZACAO, default=1)
#
#     def __str__(self):
#         return self.user.username