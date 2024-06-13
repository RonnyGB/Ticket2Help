from .models import HardwareTicket, SoftwareTicket, Ticket
import pymysql
from datetime import datetime
import uuid


def get_db_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        passwd="377024",
        db="ticketsdb"
    )


def create_ticket(ticket):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Inserir dados na tabela Tickets (comuns a todos os tipos de tickets)
    query = """
         INSERT INTO tickets (id, dtCriacao, dtUltimaAlt, colaboradorAlt ,idColaborador, estTicket, estAtendimento, 
         Tipo)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
         """
    cursor.execute(query, (
        str(ticket.id), ticket.dtCriacao, ticket.dtUltimaAlt, ticket.ColaboradorAlt, ticket.idColaborador,
        ticket.estTicket, ticket.estAtendimento, ticket.Tipo))


    if isinstance(ticket, HardwareTicket):
        query = """
            INSERT INTO hardwaretickets (id, equipamento, avaria, descRep, pecas, ticketID)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
        cursor.execute(query, (
            str(ticket.idHard), ticket.Equipamento, ticket.Avaria, ticket.DescRep, ticket.Pecas,  str(ticket.id)))

    elif isinstance(ticket, SoftwareTicket):
        query = """
            INSERT INTO softwaretickets (id, software, descNecessidade, descInt, ticketID)
            VALUES (%s, %s, %s, %s)
            """
        cursor.execute(query, (
            str(ticket.idSoft), ticket.Software, ticket.DescNecessidade,  str(ticket.id)))
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
        id, dtCriacao, dtUltimaAlt, colaboradorAlt, idColaborador, estTicket, estAtendimento, tipo = ticket_row

        if tipo == 'Hardware':
            # Consulta para buscar detalhes de hardware
            query2 = """
                SELECT id, equipamento, avaria, descRep, pecas, ticketID
                FROM HardwareTickets
                WHERE ticketID = %s
            """
            cursor.execute(query2, (id,))
            hardware_row = cursor.fetchone()

            if hardware_row:
                idHARD, equipamento, avaria, descRep, pecas, ticketID = hardware_row
                ticket = HardwareTicket()
                ticket.id = id
                ticket.dtCriacao = dtCriacao
                ticket.dtUltimaAlt = dtUltimaAlt
                ticket.idColaborador = idColaborador
                ticket.ColaboradorAlt = colaboradorAlt
                ticket.estTicket = estTicket
                ticket.estAtendimento = estAtendimento
                ticket.Tipo = tipo
                ticket.idHard = idHARD
                ticket.Equipamento = equipamento
                ticket.Avaria = avaria
                ticket.DescRep = descRep
                ticket.Pecas = pecas
                tickets.append(ticket)

        elif tipo == 'Software':
            # Consulta para buscar detalhes de software
            query2 = """
                SELECT id, software, descNecessidade, descInt
                FROM SoftwareTickets
                WHERE id = %s
            """
            cursor.execute(query2, (id,))
            software_row = cursor.fetchone()

            if software_row:
                idSOFT, software, descNecessidade, descInt = software_row
                ticket = SoftwareTicket()
                ticket.id = id
                ticket.dtCriacao = dtCriacao
                ticket.dtUltimaAlt = dtUltimaAlt
                ticket.idColaborador = idColaborador
                ticket.ColaboradorAlt = colaboradorAlt
                ticket.estTicket = estTicket
                ticket.estAtendimento = estAtendimento
                ticket.Tipo = tipo
                ticket.idSoft = idSOFT
                ticket.Software = software
                ticket.DescNecessidade = descNecessidade
                ticket.DescInt = descInt
                tickets.append(ticket)

        else:
            # Se o tipo não for reconhecido, criar um objeto Ticket genérico
            ticket = Ticket()
            tickets.append(ticket)

    cursor.close()
    conn.close()

    return tickets


# Função para listar tickets com filtros
def get_tickets(op):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Primeira consulta para buscar todos os tickets
    query1 = """
        SELECT id, dtCriacao, dtUltimaAlt, colaboradorAlt ,idColaborador, estTicket, estAtendimento, 
         Tipo
        FROM Tickets
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

    query = """
        UPDATE Tickets SET dtUltimaAlt=%s, colaboradorAlt=%s, estTicket=%s, estAtendimento=%s
        WHERE id=%s
    """
    cursor.execute(query, (
        datetime.now(), ticket.ColaboradorAlt, ticket.estTicket, ticket.estAtendimento, str(ticket.id)
    ))

    if ticket.tipo == 'hardware':
        query = """
            UPDATE HardwareTickets SET equipamento=%s, avaria=%s, descRep=%s, pecas=%s
            WHERE id=%s
        """
        cursor.execute(query, (
            ticket['equipamento'], ticket['avaria'], ticket['descRep'], ticket['pecas'], str(ticket['id'])
        ))

    elif ticket['tipo'] == 'software':
        query = """
            UPDATE SoftwareTickets SET software=%s, descNecessidade=%s, descInt=%s
            WHERE id=%s
        """
        cursor.execute(query, (
            ticket['software'], ticket['descNecessidade'], ticket['descInt'], str(ticket['id'])
        ))

    else:
        raise ValueError("Tipo de ticket não suportado")

    conn.commit()
    cursor.close()
    conn.close()
