from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.notification import views


router = SimpleRouter()
router.register(r'notifications', views.NotificationViewSet,basename="notification")

urlpatterns = [
    path('', include(router.urls)),
]
