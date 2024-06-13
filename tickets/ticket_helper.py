from .models import HardwareTicket, SoftwareTicket
import pymysql
from datetime import datetime
import uuid


def get_db_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        passwd="rrac2gbtb",
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


# Função para listar tickets com filtros
def get_tickets(filter_type):
    conn = get_db_connection()
    cursor = conn.cursor()

    if filter_type == 'hardware':
        query = """
            SELECT t.*, h.equipamento, h.avaria, h.descRep, h.pecas 
            FROM Tickets t
            JOIN HardwareTickets h ON t.id = h.id
        """
    elif filter_type == 'software':
        query = """
            SELECT t.*, s.software, s.descNecessidade, s.descInt 
            FROM Tickets t
            JOIN SoftwareTickets s ON t.id = s.id
        """
    else:
        query = "SELECT * FROM Tickets"

    cursor.execute(query)
    tickets = cursor.fetchall()

    cursor.close()
    conn.close()

    return tickets


# Função para atualizar um ticket
def update_ticket(ticket):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        UPDATE Tickets SET dtUltimaAlt=%s, colaboradorAlt=%s, estTicket=%s, estAtendimento=%s
        WHERE id=%s
    """
    cursor.execute(query, (
        datetime.now(), ticket['colaboradorAlt'], ticket['estTicket'], ticket['estAtendimento'], str(ticket['id'])
    ))

    if ticket['tipo'] == 'hardware':
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
