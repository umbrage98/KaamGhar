from django.urls import path
from .views import ApplyToJobView, MyApplicationsView, JobApplicationsListView, UpdateApplicationStatusView

urlpatterns = [
    path('apply/', ApplyToJobView.as_view(), name='apply-to-job'),
    path('applications/my/', MyApplicationsView.as_view(), name='my-applications'),
    path('<int:job_id>/applications/', JobApplicationsListView.as_view(), name='job-applications'),
    path('application/<int:pk>/update-status/', UpdateApplicationStatusView.as_view(), name='update-application-status'),
]
