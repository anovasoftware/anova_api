from rest_framework import serializers

from apps.base.models import Company

class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'company_id',
            'code',
            'description',
        ]