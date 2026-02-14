from rest_framework import serializers
from ..models import Person


class PersonSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()
    class Meta:
        model = Person
        fields = (
            'person_id',
            'first_name',
            'last_name',
            'display_name'
        )

    def get_display_name(self, obj):
        return str(obj)   # calls Person.__str__()