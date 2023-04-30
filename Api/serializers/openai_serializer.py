# myapp/serializers.py

from rest_framework import serializers

class BasicGenerationSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=255)

    def validate_prompt(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Prompt must be a string")
        return value
