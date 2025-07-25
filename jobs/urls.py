# jobs/urls.py
from django.urls import path
from .views import JobListView, JobCreateView, MyJobListView, JobDetailView

urlpatterns = [
    path('post/', JobCreateView.as_view(), name='post-job'),
    path('list/', JobListView.as_view(), name='list-jobs'),
    path('my/', MyJobListView.as_view(), name='my-job-list'),
    path('<int:pk>/', JobDetailView.as_view(), name='job-detail'),
]