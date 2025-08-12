from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'documents/upload.html', {'form': form})

def document_list(request):
    documents = Document.objects.all()
    return render(request, 'documents/list.html', {'documents': documents})
