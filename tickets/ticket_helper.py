from .models import HardwareTicket, SoftwareTicket, Ticket
import pymysql
from datetime import datetime
import uuid


def get_db_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        passwd="377024",
        db="TicketsDB"
    )


def create_ticket(tipo, id, *args):
    conn = get_db_connection()
    cursor = conn.cursor()

    if tipo == "Hardware":
        query = """
            INSERT INTO tickets_hardwareticket (ticket_ptr_id, equipamento, avaria)
            VALUES (%s, %s, %s)
            """
        cursor.execute(query, (
            id, args[0], args[1]))

    elif tipo == "Software":
        query = """
            INSERT INTO tickets_softwareticket (ticket_ptr_id, software, descNecessidade)
            VALUES (%s, %s, %s)
            """
        cursor.execute(query, (
             id, args[0], args[1]))
    else:
        raise ValueError("Tipo de ticket não suportado")

    conn.commit()
    cursor.close()
    conn.close()


def detailObj(ticket_rows):
    conn = get_db_connection()
    cursor = conn.cursor()

    tickets = []
    for ticket_row in ticket_rows:
        id, dtCriacao, dtUltimaAlt, colaboradorAlt, estTicket, estAtendimento, tipo, idColaborador = ticket_row
        if tipo == 'Hardware':
            # Consulta para buscar detalhes de hardware
            query2 = """
                SELECT equipamento, avaria, descRep, pecas
                FROM tickets_hardwareticket
                WHERE ticket_ptr_id = %s
            """
            cursor.execute(query2, (id,))
            hardware_row = cursor.fetchone()

            if hardware_row:
                equipamento, avaria, descRep, pecas = hardware_row
                ticket = HardwareTicket()
                ticket.id = id
                ticket.dtCriacao = dtCriacao.strftime('%Y-%m-%d %H:%M:%S') if dtCriacao else None
                ticket.dtUltimaAlt = dtUltimaAlt.strftime('%Y-%m-%d %H:%M:%S') if dtUltimaAlt else None
                ticket.idColaborador = idColaborador
                ticket.ColaboradorAlt = colaboradorAlt
                ticket.estTicket = estTicket
                ticket.estAtendimento = estAtendimento
                ticket.Tipo = tipo
                ticket.Equipamento = equipamento
                ticket.Avaria = avaria
                ticket.DescRep = descRep
                ticket.Pecas = pecas
                tickets.append(ticket)

        elif tipo == 'Software':
            # Consulta para buscar detalhes de software
            query2 = """
                SELECT software, descNecessidade, descInt
                FROM tickets_softwareticket
                WHERE ticket_ptr_id = %s
            """
            cursor.execute(query2, (id,))
            software_row = cursor.fetchone()

            if software_row:
                print(3)
                software, descNecessidade, descInt = software_row
                ticket = SoftwareTicket()
                ticket.id = id
                ticket.dtCriacao = dtCriacao.strftime('%Y-%m-%d %H:%M:%S') if dtCriacao else None
                ticket.dtUltimaAlt = dtUltimaAlt.strftime('%Y-%m-%d %H:%M:%S') if dtUltimaAlt else None
                ticket.idColaborador = idColaborador
                ticket.ColaboradorAlt = colaboradorAlt
                ticket.estTicket = estTicket
                ticket.estAtendimento = estAtendimento
                ticket.tipo = tipo
                ticket.software = software
                ticket.descNecessidade = descNecessidade
                ticket.descInt = descInt
                tickets.append(ticket)

        else:
            # Se o tipo não for reconhecido, criar um objeto Ticket genérico
            ticket = Ticket()
            ticket.dtCriacao = dtCriacao.strftime('%Y-%m-%d %H:%M:%S') if dtCriacao else None
            ticket.dtUltimaAlt = dtUltimaAlt.strftime('%Y-%m-%d %H:%M:%S') if dtUltimaAlt else None
            tickets.append(ticket)
    print("----------------------------------------------------------\n")
    print(tickets)
    cursor.close()
    conn.close()

    return tickets


# Função para listar tickets com filtros
def get_tickets(op):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Primeira consulta para buscar todos os tickets
    query1 = """
        SELECT id, dtCriacao, dtUltimaAlt, colaboradorAlt, estTicket, estAtendimento, 
         tipo, idColaborador_id
        FROM tickets_ticket
        """

    cursor.execute(query1)
    ticket_rows = cursor.fetchall()

    cursor.close()
    conn.close()

    lstTicket_filter = detailObj(ticket_rows)

    # Filtrar conforme a opção
    if op == 1:
        # Filtrar apenas os tickets de hardware
        lstTicket_filter = [ticket for ticket in lstTicket_filter if isinstance(ticket, HardwareTicket)]
    elif op == 2:
        # Filtrar apenas os tickets de software
        lstTicket_filter = [ticket for ticket in lstTicket_filter if isinstance(ticket, SoftwareTicket)]

    return lstTicket_filter


# Função para atualizar um ticket
def update_ticket(ticket):
    conn = get_db_connection()
    cursor = conn.cursor()

    ticket = listToObj(ticket)

    query = """
        UPDATE Tickets SET dtUltimaAlt=%s, colaboradorAlt=%s, estTicket=%s, estAtendimento=%s
        WHERE id=%s
    """
    cursor.execute(query, (
        datetime.now(), ticket.colaboradorAlt, ticket.estTicket, ticket.estAtendimento, str(ticket.id)
    ))

    if isinstance(ticket, HardwareTicket):
        query = """
            UPDATE HardwareTickets SET equipamento=%s, avaria=%s, descRep=%s, pecas=%s
            WHERE ticketID=%s
        """
        cursor.execute(query, (
            ticket.equipamento, ticket.avaria, ticket.descRep, ticket.pecas, str(ticket.id))
        )

    elif isinstance(ticket, SoftwareTicket):
        query = """
            UPDATE SoftwareTickets SET software=%s, descNecessidade=%s, descInt=%s
            WHERE ticketID=%s
        """
        cursor.execute(query, (
            ticket.software, ticket.descNecessidade, ticket.descInt, str(ticket.id)
        ))

    else:
        raise ValueError("Tipo de ticket não suportado")

    conn.commit()
    cursor.close()
    conn.close()


def listToObj(lst):

   if lst['tipo'] == 'Hardware':

       ticket = HardwareTicket()
       ticket.id = lst['id']
       ticket.dtCriacao = lst['dtCriacao']
       ticket.dtUltimaAlt = lst['dtUltimaAlt']
       ticket.idColaborador = lst['idColaborador']
       ticket.ColaboradorAlt = lst['ColaboradorAlt']
       ticket.estTicket = lst['estTicket']
       ticket.estAtendimento = lst['estAtendimento']
       ticket.tipo = lst['Tipo']
       ticket.equipamento = lst['Equipamento']
       ticket.avaria = lst['Avaria']
       ticket.descRep = lst['DescRep']
       ticket.pecas = lst['Pecas']
       return ticket

   elif lst['tipo'] == 'Software':

        ticket = SoftwareTicket()
        ticket.id = lst['id']
        ticket.dtCriacao = lst['dtCriacao']
        ticket.dtUltimaAlt = lst['dtUltimaAlt']
        ticket.idColaborador = lst['idColaborador']
        ticket.ColaboradorAlt = lst['ColaboradorAlt']
        ticket.estTicket = lst['estTicket']
        ticket.estAtendimento = lst['estAtendimento']
        ticket.tipo = lst['Tipo']
        ticket.software = lst['Software']
        ticket.descNecessidade = lst['DescNecessidade']
        ticket.descInt = lst['DescInt']
        return ticket





