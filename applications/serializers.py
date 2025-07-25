from rest_framework import serializers
from .models import Application
from jobs.serializers import JobSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# Serializer for User details (customize fields as needed)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields ='__all__'  # add any fields you want to expose

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'job', 'applicant', 'applied_at']
        read_only_fields = ['applicant', 'applied_at', 'status']
        
class ApplicationDetailSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    applicant = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'job', 'applicant', 'applied_at', 'status']

