from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("storage/", include("storage.urls")),
]


if settings.ENABLE_BROWSABLE_API:
    urlpatterns.extend(path('api-auth/', include('rest_framework.urls')))

urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
