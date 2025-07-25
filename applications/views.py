from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Application
from .serializers import ApplicationSerializer, ApplicationDetailSerializer
from jobs.models import Job

class ApplyToJobView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, 'kyc') or not user.kyc.verified:
            raise PermissionDenied("You must complete KYC verification to apply for jobs.")
        if user.user_type != 'employee':
            raise PermissionDenied("Only employees can apply to jobs.")
        serializer.save(applicant=user)


class MyApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user).order_by('-applied_at')


class JobApplicationsListView(generics.ListAPIView):
    serializer_class = ApplicationDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        user = self.request.user

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            raise PermissionDenied("Job not found.")

        if job.posted_by != user:
            raise PermissionDenied("You do not have permission to view applications for this job.")

        return Application.objects.filter(job=job).order_by('-applied_at')

class UpdateApplicationStatusView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        app = super().get_object()
        if app.job.posted_by != self.request.user:
            raise PermissionDenied("You cannot update this application.")
        return app

    def update_credit_score(self, app):
        business_user = app.job.posted_by
        applicant_user = app.user

        if app.status == "accepted":
            applicant_user.credit_score = (applicant_user.credit_score or 0) + 10
            applicant_user.save()
        elif app.status == "rejected":
            business_user.credit_score = (business_user.credit_score or 0) + 0  # No reward
            business_user.save()

    def put(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)

        app = self.get_object()
        self.update_credit_score(app)

        return response