from .clases import Monitor
from rest_framework import serializers


class monitorSerializer(serializers.Serializer):
    cpu = serializers.CharField(max_length=10)
    memoria = serializers.CharField(max_length=10)
    disco = serializers.CharField(max_length=10)
