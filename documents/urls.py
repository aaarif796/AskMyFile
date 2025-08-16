from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, document_list

router = DefaultRouter()
router.register(r'documents', DocumentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', document_list, name='document-list'), 
]
