from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin


schema_view = get_schema_view(
   openapi.Info(
      title="iClean Platform API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="swiftv99@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.IsAuthenticatedOrReadOnly],
)

admin.site.site_header = "iClean Administration"
admin.site.site_title = "iClean Administration"
admin.site.index_title = "iClean Platform"