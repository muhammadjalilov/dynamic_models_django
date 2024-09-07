from django.contrib.auth.models import User
from django.db import models


class FormModel(models.Model):
    form_name = models.CharField(max_length=256, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forms")
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.form_name


class FieldModel(models.Model):
    FIELD_TYPE_CHOICES = (("int", "Integer"), ("str", "String"), ("bool", "Boolean"))
    form = models.ForeignKey(FormModel, on_delete=models.CASCADE, related_name="fields")
    name = models.CharField(max_length=256)
    field_type = models.CharField(max_length=4, choices=FIELD_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name}-{self.field_type}"
