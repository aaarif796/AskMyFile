from rest_framework import serializers

class GenerateRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=5000)
    model = serializers.CharField(default="llama2")  # default Ollama model
