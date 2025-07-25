from django.core.management.base import BaseCommand
from applications.models import Application
from django.utils.timezone import now
from datetime import timedelta

class Command(BaseCommand):
    help = 'Penalize businesses who didn’t respond in 3 days'

    def handle(self, *args, **kwargs):
        three_days_ago = now() - timedelta(days=3)
        pending_apps = Application.objects.filter(status="pending", created_at__lte=three_days_ago)

        for app in pending_apps:
            business = app.job.posted_by
            business.credit_score = max((business.credit_score or 0) - 10, 0)
            business.save()
            self.stdout.write(f"Penalized {business.email} for not responding to application ID {app.id}")
