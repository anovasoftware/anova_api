from rest_framework import serializers

from apps.res.models import ClientExtension
from apps.static.models import Client


class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'client_id',
            'code',
            'description',
        )


class ClientExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientExtension
        fields = (
            'client_extension_id',
            'currency_id',
        )


class ClientDetailSerializer(serializers.ModelSerializer):
    client_extension = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = (
            'client_id',
            'code',
            'description',
            'client_extension'
        )

    def get_client_extension(self, client):
        client_extension = client.client_extensions.first()

        if not client_extension:
            return None

        return ClientExtensionSerializer(client_extension).data
