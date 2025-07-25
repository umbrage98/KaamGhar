from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job
from .serializers import JobSerializer

class JobCreateView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, 'kyc') or not user.kyc.verified:
            raise PermissionDenied("You must complete KYC verification to post a job.")
        if user.user_type != 'business':
            raise PermissionDenied("Only business users can post jobs.")
        serializer.save(posted_by=user)


from rest_framework.filters import SearchFilter


class JobListView(generics.ListAPIView):
    queryset = Job.objects.all().order_by('-posted_at')
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type', 'location', 'company']
    search_fields = ['title', 'company', 'location', 'posted_by__full_name']  # Search by organization name

class MyJobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user).order_by('-posted_at')
# jobs/views.py
class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]  # Allow public access for job listings