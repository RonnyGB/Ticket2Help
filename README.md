
# Ticket2Help

Ticket2Help é um sistema de gestão de tickets desenvolvido em Django.

# Funcionalidades

- Criação de Tickets: Permite a criação de tickets de hardware e software.
- Atualização de Tickets: Atualiza status e detalhes técnicos dos tickets.
- Listagem de Tickets: Lista todos os tickets com filtros por tipo.
- Gerenciamento de Usuários: Administra permissões e atividades dos colaboradores.

#Requisitos

- Python 3.6+
- Django 3.2+
- MySQL

#Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/RonnyGB/Ticket2Help.git
   cd Ticket2Help
   ```

2. Crie e ative um ambiente virtual:
   ```sh
   python -m venv .venv
   .\env\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

4. Configure o banco de dados no arquivo `Ticket2Help_P4/settings.py`.

5. Crie as migrações:
   ```sh
   python manage.py makemigrations 'app_name'
   ```
   
6. Execute as migrações:
   ```sh
   python manage.py migrate
   ```

7. Inicie o servidor de desenvolvimento:
   ```sh
   python manage.py runserver
   ```

# Documentação

A documentação do projeto está disponível no diretório `docs` e pode ser gerada usando o Sphinx:
```sh
cd docs
.\make.bat html  # Windows
make html  # macOS/Linux
```

# Contribuição

Contribuições são bem-vindas! Veja o arquivo `contributing.rst` para mais detalhes sobre como contribuir.

# Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---
