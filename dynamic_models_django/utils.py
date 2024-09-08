from django.db import DEFAULT_DB_ALIAS, connections, models
from django.utils.text import slugify

from dynamic_models_django.config import dynamic_models_app_label


class DynamicTableCreator:
    def __init__(self, form_model):
        self.form_model = form_model
        self.db_name = DEFAULT_DB_ALIAS

    def create_table(self):
        table_name = self._get_table_name()
        fields = self._get_fields()

        with connections[self.db_name].schema_editor() as editor:
            model = self._generate_model(table_name, fields)
            editor.create_model(model)

    def _get_table_name(self):
        return f"{dynamic_models_app_label()}_{slugify(self.form_model.form_name).replace('-', '_')}".lower()

    def _get_fields(self):
        fields = {
            "id": models.AutoField(primary_key=True),
        }

        for field in self.form_model.fields.all():
            if field.field_type == "int":
                fields[field.name] = models.IntegerField()
            elif field.field_type == "str":
                fields[field.name] = models.CharField(max_length=256)
            elif field.field_type == "bool":
                fields[field.name] = models.BooleanField(default=True)
        return fields

    def _generate_model(self, table_name, fields):
        app_label = dynamic_models_app_label()

        class Meta:
            db_table = table_name

        attrs = {
            "__module__": app_label,
            "Meta": Meta,
            **fields,
        }

        return type(table_name, (models.Model,), attrs)


registered_models = []
