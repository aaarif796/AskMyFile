from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import Document
from .serializers import DocumentSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

def document_list(request):
    documents = Document.objects.all()
    return render(request, 'documents/index.html', {'documents': documents})

def document_upload(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')
        if title and file:
            Document.objects.create(title=title, file=file)
            return redirect('document-list')
    return render(request, 'documents/upload.html')
