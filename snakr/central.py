from django.apps import AppConfig
import secure.settings as settings
import logger

class Config(AppConfig):

    name = settings.GAE_APP_NAME
    verbose_name = name
    log = logger.Loggr()

    def ready(self):
        # startup code here
        pass