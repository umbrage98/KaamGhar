# kyc/admin.py
from datetime import timezone
from django.contrib import admin
from .models import KYC

@admin.register(KYC)
class KYCAdmin(admin.ModelAdmin):
    list_display = ('user', 'verified', 'submitted_at', 'verified_at')
    list_filter = ('verified',)
    actions = ['mark_verified']

    def mark_verified(self, request, queryset):
        queryset.update(verified=True, verified_at=timezone.now())
    mark_verified.short_description = "Mark selected KYCs as verified"
