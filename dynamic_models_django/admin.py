from django.contrib import admin
from django.contrib.admin import TabularInline

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


def register_dynamic_model(dynamic_model=None):
    models = [dynamic_model]
    for model in models:
        if model not in admin.site._registry:
            admin.site.register(model, DynamicAdmin)
