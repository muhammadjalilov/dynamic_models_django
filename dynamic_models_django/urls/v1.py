from django.urls import path, include
from rest_framework.routers import DefaultRouter

from dynamic_models_django.api import get_dynamic_viewset

router = DefaultRouter()
# dynamic_viewset = get_dynamic_viewset()

urlpatterns = [
    path('api/', include(router.urls)),
]