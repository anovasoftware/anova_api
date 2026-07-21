from rest_framework import serializers
from apps.res.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'event_id',
            'code',
            'description',
            'event_start_date',
            'event_end_date',
            'status_id',
        )