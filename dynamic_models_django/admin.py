from django.apps import apps
from django.contrib import admin
from django.contrib.admin import TabularInline
from django.db.models import Model

from dynamic_models_django.config import dynamic_models_app_label
from dynamic_models_django.models import FieldModel, FormModel


class FieldModelInline(TabularInline):
    model = FieldModel
    extra = 1


@admin.register(FormModel)
class FormModelAdmin(admin.ModelAdmin):
    list_display = ("form_name", "created_by", "modified_at")
    search_fields = ("form_name", "created_by__username")
    inlines = [
        FieldModelInline,
    ]


@admin.register(FieldModel)
class FieldModelAdmin(admin.ModelAdmin):
    list_display = ("name", "form", "field_type")
    list_filter = ("form", "field_type")
    search_fields = ("name", "form__form_name")


class DynamicAdmin(admin.ModelAdmin):
    pass


def register_dynamic_model(table_name):
    dynamic_model = apps.get_model(dynamic_models_app_label(), table_name)
    print(issubclass(dynamic_model,Model))
    admin.site.register(dynamic_model, DynamicAdmin)
