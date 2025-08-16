from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, document_list, document_upload

router = DefaultRouter()
router.register(r'documents', DocumentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', document_list, name='document-list'), 
    path('upload/', document_upload, name='document-upload'),
]
