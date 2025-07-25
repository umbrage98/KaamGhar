# kyc/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class KYC(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='kyc')
    full_namee = models.CharField(max_length=255)
    id_number = models.CharField(max_length=20)  # 🔁 Changed to CharField for flexibility
    id_document = models.FileField(upload_to='kyc_docs/')
    issued_place = models.CharField(max_length=255, blank=True, null=True)  # ✅ New field
    verified = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    registration_number = models.CharField(max_length=20,blank=True, null=True ) 

    def __str__(self):
        return f"KYC for {self.user.username} - Verified: {self.verified}"
