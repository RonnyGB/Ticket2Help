"""
Configurações do Django para o projeto Ticket2Help_P4.

Gerado por 'django-admin startproject' usando Django 4.2.13.

Para mais informações sobre este arquivo, veja
https://docs.djangoproject.com/en/4.2/topics/settings/

Para a lista completa de configurações e seus valores, veja
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

"""# Constroi caminhos dentro do projeto como este: BASE_DIR / 'subdir'."""
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações de desenvolvimento de início rápido - não são adequadas para produção
# Veja https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# AVISO DE SEGURANÇA: mantenha a chave secreta usada na produção em segredo!
SECRET_KEY = 'django-inseguro-p7=la)9*wy%sq)ehfh*lu*8yejuuoj$is!lg(ijp!k@#(9dj!n'

# AVISO DE SEGURANÇA: não execute com o debug ativado em produção!
DEBUG = True

ALLOWED_HOSTS = []

# Definição da aplicação
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tickets',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Ticket2Help_P4.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Ticket2Help_P4.wsgi.application'

# Banco de dados
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'TicketsDB',
        'USER': 'root',
        'PASSWORD': '377024',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Validação de senha
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internacionalização
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Arquivos estáticos (CSS, JavaScript, Imagens)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Tipo de campo de chave primária padrão
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
