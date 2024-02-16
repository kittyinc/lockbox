from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from storage import views_api, views_client

router = SimpleRouter()
router.register(r'files', views_api.FileModelViewSet)

chunk_router = NestedSimpleRouter(router, r'files', lookup="file")
chunk_router.register(r'chunks', views_api.FileChunkViewSet, basename="file-chunks")

urlpatterns = [
    re_path(r"api/", include(router.urls)),
    re_path(r"api/", include(chunk_router.urls)),
    path("client/files/", views_client.FileUploadView.as_view, name="client-fileupload"),
]
