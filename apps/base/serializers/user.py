from rest_framework import serializers
from ..models import User
from .person import PersonSerializer

class UserSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    class Meta:
        model = User
        fields = ('user_id', 'username', 'person')
