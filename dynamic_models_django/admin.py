from django.contrib import admin
from django.contrib.admin import TabularInline

from dynamic_models_django.models import FieldModel, FormModel
from dynamic_models_django.utils import DynamicTableCreator, registered_models


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


def register_dynamic_models():
    for form_model in FormModel.objects.all():
        creator = DynamicTableCreator(form_model)
        dynamic_model = creator._generate_model(
            creator._get_table_name(), creator._get_fields()
        )
        # dynamic_model = apps.get_model(dynamic_models_app_label(),creator._get_table_name())  # xato berdi app rerundan keyin uchib ketadi dynamic modellar
        model_name = dynamic_model._meta.object_name

        if model_name not in registered_models:
            try:
                class DynamicModelAdmin(admin.ModelAdmin):
                    list_display = [field.name for field in dynamic_model._meta.fields]

                admin.site.register(dynamic_model, DynamicModelAdmin)
                registered_models.append(model_name)
            except admin.sites.AlreadyRegistered:
                pass


register_dynamic_models()
