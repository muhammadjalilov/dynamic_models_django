from django.apps import apps
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

from dynamic_models_django.config import dynamic_models_app_label


def get_dynamic_serializer(table_name):
    dynamic_model = apps.get_model(dynamic_models_app_label(), table_name)

    class DynamicSerializer(serializers.ModelSerializer):
        class Meta:
            model = dynamic_model
            fields = "__all__"

    return DynamicSerializer


def get_dynamic_viewset(table_name):
    dynamic_model = apps.get_model(dynamic_models_app_label(), table_name)
    dynamic_serializer = get_dynamic_serializer(table_name)

    class DynamicViewSet(ModelViewSet):
        queryset = dynamic_model.objects.all()
        serializer_class = dynamic_serializer

    return DynamicViewSet
