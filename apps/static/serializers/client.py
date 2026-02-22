from rest_framework import serializers
from apps.static.models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'client_id',
            'code',
            'description'
        )
