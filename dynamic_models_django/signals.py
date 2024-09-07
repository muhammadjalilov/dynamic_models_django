from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from dynamic_models_django.admin import register_dynamic_model
from dynamic_models_django.config import dynamic_models_app_label
from dynamic_models_django.models import FormModel
from dynamic_models_django.utils import DynamicTableCreator


@receiver(post_save, sender=FormModel)
def create_table_after_form_save(sender, instance, created, **kwargs):
    if created:
        table_name = f"{dynamic_models_app_label()}_{slugify(instance.form_name).replace('-', '_')}".lower()
        transaction.on_commit(lambda: create_and_register_model(instance, table_name))


def create_and_register_model(instance, table_name):
    dynamic_creator = DynamicTableCreator(instance)
    dynamic_creator.create_table()
    register_dynamic_model(table_name)
