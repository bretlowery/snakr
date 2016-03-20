from django.apps import AppConfig

@staticmethod
class Config(AppConfig):

    name = 'snakr'
    verbose_name = name

    def ready(self):
        pass

