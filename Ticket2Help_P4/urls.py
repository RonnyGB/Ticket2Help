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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('home/list_tickets/', list_tickets, name='list_tickets'),
    path('accounts/register/', register, name='register'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
]

