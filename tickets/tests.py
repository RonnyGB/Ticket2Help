from tickets.models import HardwareTicket
from tickets.models import SoftwareTicket
from ticket_helper import *

ticket = HardwareTicket()
ticket.Equipamento = "Computador"

ticket2 = SoftwareTicket()
ticket2.idColaborador = "12345678"
ticket2.DescInt = "Type sHI"

print(ticket.printTicket())
print("----------------")
print(ticket2.printTicket())


create_ticket(ticket)