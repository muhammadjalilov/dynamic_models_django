from django.apps import AppConfig
from django.db.models.signals import post_migrate



class DynamicModelsDjangoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dynamic_models_django"

    def ready(self):
        import dynamic_models_django.signals

