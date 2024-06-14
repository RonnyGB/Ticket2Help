Usage
=====

Esta seção explica como usar o TICKET2HELP.

Configuração:
-------------
Para configurar o TICKET2HELP, siga os passos abaixo:

1. **Configuração do Ambiente Virtual**:
   - Crie e ative um ambiente virtual:
     ```sh
     python -m venv Ticket2Help.venv
     source Ticket2Help.venv/bin/activate  # Para Windows use: Ticket2Help.venv\Scripts\activate
     ```

2. **Instalação das Dependências**:
   - Instale as dependências listadas no arquivo `requirements.txt`:
     ```sh
     pip install -r requirements.txt
     ```

3. **Configuração do Banco de Dados**:
   - Configure o banco de dados no arquivo `settings.py`:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'TicketsDB',
             'USER': 'root',
             'PASSWORD': 'sua_senha',
             'HOST': '127.0.0.1',
             'PORT': '3306',
         }
     }
     ```
   - Execute as migrações do banco de dados:
     ```sh
     python manage.py migrate
     ```

4. **Inicialização do Servidor**:
   - Inicie o servidor de desenvolvimento:
     ```sh
     python manage.py runserver
     ```

Exemplos de Uso:
----------------
 Como usar o TICKET2HELP:

1. **Criar um Novo Ticket**:
   - Acesse a página de criação de tickets e preencha os detalhes necessários, como tipo de ticket (hardware ou software), descrição e prioridade.
   - Submeta o formulário para criar o ticket.

2. **Atualizar um Ticket Existente**:
   - Acesse a lista de tickets e selecione o ticket que deseja atualizar.
   - Edite as informações necessárias e salve as alterações.

3. **Visualizar Detalhes do Ticket**:
   - Acesse a lista de tickets e clique em um ticket específico para ver os detalhes completos, incluindo histórico de alterações e status atual.

4. **Gerar Relatórios**:
   - Use a funcionalidade de geração de relatórios para obter estatísticas e análises sobre os tickets abertos, fechados, em andamento, etc.

5. **Gerenciamento de Usuários**:
   - Acesse a interface de administração para gerenciar usuários, atribuir permissões e visualizar atividades dos colaboradores.

