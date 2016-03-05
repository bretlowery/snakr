from django.apps import AppConfig

@staticmethod
class Config(AppConfig):

    name = 'snakrv2'
    verbose_name = name

    def ready(self):
        pass

