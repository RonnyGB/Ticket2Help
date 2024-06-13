from django.apps import AppConfig


class NetflixConfig(AppConfig):
    name = 'Ticket2Help_P4'

    def ready(self):
        import tickets.signals