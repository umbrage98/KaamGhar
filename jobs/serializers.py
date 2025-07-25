# jobs/serializers.py
from rest_framework import serializers
from .models import Job
from user.serializers import UserSerializer

class JobSerializer(serializers.ModelSerializer):
    posted_by = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ['id', 'title', 'company', 'location', 'type', 'salary', 'posted_at', 'description', 'posted_by']
        read_only_fields = ['posted_at', 'posted_by']

    def get_posted_by(self, obj):
        # Return limited organization details for the user who posted the job
        user = obj.posted_by
        return {
            'id': str(user.id),  # UUID as string
            'full_name': user.full_name or user.username,  # Use full_name or fallback to username
            'industry': user.industry,
            'location': user.location,
            'credit_score': user.credit_score,
        }