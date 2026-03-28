from rest_framework import serializers
from apps.static.models import Menu

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = (
            'menu_id',
            'description',
            'hotel_required'
        )
