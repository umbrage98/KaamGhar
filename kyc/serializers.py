# kyc/serializers.py
from rest_framework import serializers
from .models import KYC

class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = ['id', 'user', 'full_namee', 'id_document', 'verified', 'submitted_at', 'verified_at','id_number','registration_number','issued_place']
        read_only_fields = ['verified', 'submitted_at', 'verified_at', 'user']
