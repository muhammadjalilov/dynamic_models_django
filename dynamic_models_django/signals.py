from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from dynamic_models_django.models import FormModel
from dynamic_models_django.utils import DynamicTableCreator


@receiver(post_save, sender=FormModel)
def create_table_after_form_save(sender, instance, created, **kwargs):
    from dynamic_models_django.config import dynamic_models_app_label

    if created:
        transaction.on_commit(lambda: create_and_register_model(instance))


def create_and_register_model(instance):
    dynamic_creator = DynamicTableCreator(instance)
    dynamic_creator.create_table()
