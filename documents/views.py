from django.shortcuts import render
from rest_framework import viewsets
from .models import Document
from .serializers import DocumentSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

def document_list(request):
    documents = Document.objects.all()  # Pass documents to template
    return render(request, 'documents/', {'documents': documents})
