from rest_framework import serializers
from apps.base.models import Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'role_id',
            'description'
        )
