# kyc/views.py
from rest_framework import generics, permissions
from .models import KYC
from .serializers import KYCSerializer
from rest_framework.exceptions import NotFound
class SubmitKYCView(generics.CreateAPIView):
    serializer_class = KYCSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Attach user automatically
        serializer.save(user=self.request.user)
        
class MyKYCDetailView(generics.RetrieveAPIView):
    serializer_class = KYCSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.kyc
        except KYC.DoesNotExist:
            raise NotFound(detail="KYC record not found for this user.")
class KYCDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = KYCSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Return the current user's KYC instance
        return self.request.user.kyc