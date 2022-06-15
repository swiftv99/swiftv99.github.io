from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.service import views


router = SimpleRouter()
router.register(r'services', views.ServiceViewSet,basename="service")

urlpatterns = [
    path('', include(router.urls)),
]

