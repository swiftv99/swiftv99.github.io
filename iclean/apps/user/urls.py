from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.notification.urls import router as notification_router
from apps.request.urls import router as request_router
from apps.review.urls import router as review_router
from apps.service.urls import router as service_router
from apps.user.views import role, user, client, company
from apps.user.views.register import RegisterUserView, ChangePasswordView, LogoutView, LogoutAllView


router = DefaultRouter()
router.registry.extend(notification_router.registry)
router.registry.extend(request_router.registry)
router.registry.extend(review_router.registry)
router.registry.extend(service_router.registry)

router.register(r'roles', role.RoleViewSet, basename="role")
router.register(r'users', user.UserViewSet, basename="user")
router.register(r'clients', client.ClientViewSet, basename="client")
router.register(r'companys', company.CompanyViewSet, basename="company")


urlpatterns = [
    path('', include(router.urls)),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('users/<int:pk>/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-all/', LogoutAllView.as_view(), name='logout_all'),
]