from django.shortcuts import render
from django.http import JsonResponse
from .retrieval import query_index

def ask_chatbot(request):
    question = request.GET.get('q')
    if not question:
        return JsonResponse({'error': 'No question provided'}, status=400)
    answers = query_index(question)
    return JsonResponse({'answers': answers})
