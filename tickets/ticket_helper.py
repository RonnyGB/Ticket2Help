from .models import HardwareTicket, SoftwareTicket, Ticket
import pymysql
from datetime import datetime
import uuid

def get_db_connection():
    """
    Estabelece uma conexão com o banco de dados MySQL.
    """
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        passwd="rrac2gbtb",
        db="TicketsDB"
    )

def create_ticket(tipo, id, *args):
    """
    Cria um novo ticket no banco de dados.
    
    Args:
        tipo (str): Tipo do ticket (Hardware ou Software).
        id (str): ID do ticket.
        *args: Argumentos adicionais necessários para a criação do ticket.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    if tipo == "Hardware":
        query = """
            INSERT INTO tickets_hardwareticket (ticket_ptr_id, equipamento, avaria)
            VALUES (%s, %s, %s)
            """
        cursor.execute(query, (id, args[0], args[1]))

    elif tipo == "Software":
        query = """
            INSERT INTO tickets_softwareticket (ticket_ptr_id, software, descNecessidade)
            VALUES (%s, %s, %s)
            """
        cursor.execute(query, (id, args[0], args[1]))
    else:
        raise ValueError("Tipo de ticket não suportado")

    conn.commit()
    cursor.close()
    conn.close()

def detailObj(ticket_rows):
    """
    Converte os dados das linhas de tickets em objetos de tickets detalhados.
    
    Args:
        ticket_rows (list): Linhas de tickets.
    
    Returns:
        list: Lista de objetos de tickets detalhados.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    tickets = []

    for ticket_row in ticket_rows:
        id, dtCriacao, dtUltimaAlt, colaboradorAlt, estTicket, estAtendimento, tipo, idColaborador = ticket_row
        if tipo == 'Hardware':
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
            query2 = """
                SELECT software, descNecessidade, descInt
                FROM tickets_softwareticket
                WHERE ticket_ptr_id = %s
            """
            cursor.execute(query2, (id,))
            software_row = cursor.fetchone()

            if software_row:
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
            ticket = Ticket()
            ticket.dtCriacao = dtCriacao.strftime('%Y-%m-%d %H:%M:%S') if dtCriacao else None
            ticket.dtUltimaAlt = dtUltimaAlt.strftime('%Y-%m-%d %H:%M:%S') if dtUltimaAlt else None
            tickets.append(ticket)
    
    cursor.close()
    conn.close()

    return tickets

def get_tickets(op):
    """
    Lista os tickets com base na opção de filtro.
    
    Args:
        op (int): Opção de filtro (1 para Hardware, 2 para Software, 0 para todos).
    
    Returns:
        list: Lista de tickets filtrados.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

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

    if op == 1:
        lstTicket_filter = [ticket for ticket in lstTicket_filter if isinstance(ticket, HardwareTicket)]
    elif op == 2:
        lstTicket_filter = [ticket for ticket in lstTicket_filter if isinstance(ticket, SoftwareTicket)]

    return lstTicket_filter

def update_ticket(ticket):
    """
    Atualiza um ticket no banco de dados.
    
    Args:
        ticket (dict): Dados do ticket a ser atualizado.
    """
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
    """
    Converte uma lista de dados em um objeto Ticket.
    
    Args:
        lst (dict): Dados do ticket em formato de lista.
    
    Returns:
        object: Objeto Ticket correspondente aos dados fornecidos.
    """
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
