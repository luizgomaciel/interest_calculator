from rest_framework import serializers

class InitialProjectSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True, required=False)