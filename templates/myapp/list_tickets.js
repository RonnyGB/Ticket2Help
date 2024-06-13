<!DOCTYPE html>
<html>
<head>
    <title>Lista de Tickets</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        /* Estilos para o modal */
        .modal {
            display: none; /* Esconde o modal por padrão */
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.4); /* Fundo semi-transparente */
        }
        .modal-content {
            background-color: #fefefe;
            margin: 15% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 80%;
            max-width: 600px;
        }
        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
        }
        .close:hover,
        .close:focus {
            color: black;
            text-decoration: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Lista de Tickets</h1>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Data de Criação</th>
                <th>ID do Colaborador</th>
                <th>Estado do Ticket</th>
                <th>Estado do Atendimento</th>
                <th>Tipo</th>
                <th>Detalhes</th>
            </tr>
        </thead>
        <tbody>
            {% for ticket in tickets %}
                <tr>
                    <td>{{ ticket.id }}</td>
                    <td>{{ ticket.dtCriacao }}</td>
                    <td>{{ ticket.idColaborador }}</td>
                    <td>{{ ticket.estTicket }}</td>
                    <td>{{ ticket.estAtendimento }}</td>
                    <td>{{ ticket.Tipo }}</td>
                    <td><a href="#" onclick="showDetails('{{ ticket.id }}', '{{ ticket.dtCriacao}}', '{{ ticket.idColaborador }}', '{{ ticket.estTicket }}', '{{ ticket.estAtendimento }}','{{ ticket.Tipo }}'); return false;">Detalhes</a></td>
                </tr>
            {% endfor %}
        </tbody>
    </table>

    <!-- Modal -->
    <div id="myModal" class="modal">
        <!-- Conteúdo do modal -->
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <h2>Detalhes do Ticket</h2>
            <p id="ticketDetails"></p>
        </div>
    </div>

    <!-- Script para manipulação do modal -->
    <script>
        // Função para exibir o modal com os detalhes do ticket
        function showDetails(id, dtCriacao, idColaborador, estTicket, estAtendimento, Tipo) {
            var modal = document.getElementById('myModal');
            var ticketDetails = document.getElementById('ticketDetails');

            // Limpa o conteúdo anterior
            ticketDetails.innerHTML = '';

            // Converte a string JSON de volta para um objeto JavaScript
            var ticket = JSON.parse(ticketJson);

            // Adiciona as informações do ticket ao modal
            var details = "<strong>ID do Ticket:</strong> " + id + "<br>" +
                          "<strong>Data de Criação:</strong> " + dtCriacao + "<br>" +
                          "<strong>ID do Colaborador:</strong> " + idColaborador + "<br>" +
                          "<strong>Estado do Ticket:</strong> " + estTicket + "<br>" +
                          "<strong>Estado do Atendimento:</strong> " + estAtendimento + "<br>" +
                          "<strong>Tipo:</strong> " + Tipo;

            ticketDetails.innerHTML = details;

            modal.style.display = 'block'; // Exibe o modal
        }

        // Função para fechar o modal
        function closeModal() {
            var modal = document.getElementById('myModal');
            modal.style.display = 'none'; // Esconde o modal
        }
    </script>


</body>
</html>