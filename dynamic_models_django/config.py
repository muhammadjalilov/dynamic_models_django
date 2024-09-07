from django.conf import settings

from dynamic_models_django.apps import DynamicModelsDjangoConfig


def dynamic_models_app_label():
    return _settings().get("USE_APP_LABEL", DynamicModelsDjangoConfig.name)


def _settings():
    return getattr(settings, "DYNAMIC_MODELS", {})
