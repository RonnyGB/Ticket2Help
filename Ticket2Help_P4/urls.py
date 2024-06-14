"""
URL configuration for Ticket2Help_P4 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tickets.views import index
from tickets.views import list_tickets
from tickets.views import register
from tickets.views import login_view
from tickets.views import logout_view
from tickets.views import home
from tickets.views import new_ticket
from tickets.views import ticket_details
from tickets.views import manage_tickets
from tickets.views import edit_ticket
from tickets.views import tickets_atendidos_por_data
from tickets.views import tickets_atendidos
from tickets.views import tickets_resolvidos
from tickets.views import media_tempo_atendimento


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('home/client/list_tickets/', list_tickets, name='list_tickets'),
    path('home/client/ticket_details/<uuid:ticket_id>/', ticket_details, name='ticket_details_client'),
    path('home/client/new_ticket/', new_ticket, name='new_ticket'),
    path('home/technic/ticket_details/<uuid:ticket_id>/', ticket_details, name='ticket_details_technic'),
    path('home/technic/manage_tickets', manage_tickets, name='manage_tickets'),
    path('home/technic/edit_ticket/<uuid:ticket_id>/', edit_ticket, name='edit_ticket'),
    path('accounts/register/', register, name='register'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('home/technic/gen_report/', tickets_atendidos, name='tickets_atendidos'),
    path('home/technic/gen_report2/', tickets_resolvidos, name='tickets_resolvidos'),
    path('home/technic/gen_report3/', media_tempo_atendimento, name='media_tempo_atendimento'),
]

