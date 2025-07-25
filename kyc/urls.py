# jobs/urls.py

from django.urls import path
from .views import MyKYCDetailView, KYCDetailUpdateView, SubmitKYCView

urlpatterns = [
    path('create/', SubmitKYCView.as_view(), name='post-job'),
    path('update/', KYCDetailUpdateView.as_view(), name='post-job'),
    path('details/', MyKYCDetailView.as_view(), name='list-jobs'),
]
