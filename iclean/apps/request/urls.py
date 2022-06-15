from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.request import views


router = SimpleRouter()
router.register(r'requests', views.RequestViewSet,basename="request")
router.register(r'request-statuses', views.RequestStatusViewSet,basename="requeststatus")

urlpatterns = [
    path('', include(router.urls)),
]