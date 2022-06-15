from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.review import views


router = SimpleRouter()
router.register(r'reviews', views.ReviewViewSet,basename="review")

urlpatterns = [
    path('', include(router.urls)),
]