# myapp/views.py

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from Api.serializers import BasicGenerationSerializer
import openai

openai.api_key = "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"

def BasicGeneration(userPrompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": userPrompt}]
    )
    
    return completion.choices[0].message.content

class BasicGenerationView(CreateAPIView):
    serializer_class = BasicGenerationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        prompt = serializer.validated_data.get('prompt')
        response = BasicGeneration(prompt)
        return Response({'response': response})
