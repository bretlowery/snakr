from django.apps import AppConfig

class Config(AppConfig):

    name = 'snakr'
    verbose_name = name

    def ready(self):
        pass

