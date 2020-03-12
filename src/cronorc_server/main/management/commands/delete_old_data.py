from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings

from datetime import timedelta

from ...models import Job, Execution


class Command(BaseCommand):

    help = 'Deletes old job executions'

    def handle(self, *args, **options):
        for job in Job.objects.iterator():
            deleted = self.delete_by_date(job) + self.delete_by_amount(job)
            self.stdout.write(f'{job} - {deleted} records were deleted')

    def delete_by_date(self, job):
        cutoff = timezone.now() - timedelta(days=settings.MAX_DAYS_TO_KEEP)
        qs = job.execution_set.filter(start__lt=cutoff)
        return qs.delete()[0]

    def delete_by_amount(self, job):
        qs = job.execution_set.order_by('-id')
        if qs.count() <= settings.MAX_AMOUNT_TO_KEEP:
            return 0
        last_id = qs[settings.MAX_AMOUNT_TO_KEEP].id
        return qs.filter(id__lt=last_id).delete()[0]
