from django.urls import include, path
from django.utils.text import slugify
from rest_framework.routers import DefaultRouter

from dynamic_models_django.api import get_dynamic_viewset
from dynamic_models_django.config import dynamic_models_app_label
from dynamic_models_django.models import FormModel

router = DefaultRouter()

models = FormModel.objects.all()
for i in models:
    table_name = (
        f"{dynamic_models_app_label()}_{slugify(i.form_name).replace('-', '_')}".lower()
    )
    dynamic_viewset = get_dynamic_viewset(table_name)
    router.register(rf"{table_name}", dynamic_viewset, basename=table_name)


urlpatterns = [
    path("api/", include(router.urls)),
]
