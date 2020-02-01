from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from djchoices import DjangoChoices, ChoiceItem


class JobStatus(DjangoChoices):

    OK       = ChoiceItem()
    DELAYED  = ChoiceItem()
    FLAPPING = ChoiceItem()
    FAILED   = ChoiceItem()


class Job(models.Model):

    hostname = models.CharField(max_length=255, db_index=True)
    ip = models.GenericIPAddressField()
    command = models.TextField(db_index=True)
    status = models.CharField(max_length=10, db_index=True, choices=JobStatus.choices, default=JobStatus.OK)
    last_execution = models.DateTimeField(null=True)
    last_notification = models.DateTimeField(null=True)
    display_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ('hostname', 'ip', 'command')

    def __str__(self):
        name = self.get_display_name()
        name = name[:100] + '...' if len(name) > 100 else name
        return f'{self.hostname} [{self.ip}] {name}'

    def get_display_name(self):
        return self.display_name or self.command

    def get_absolute_url(self):
        return reverse('job', args=[self.id])

    def update_status(self):
        new_status = self.status
        executions = self.execution_set.order_by('-id')[:5]
        if executions[0].success():
            new_status = JobStatus.OK
        else:
            new_status = JobStatus.FAILED
        # TODO identify flapping and delayed jobs
        if new_status != self.status:
            self.send_alert(self.status, new_status)
            self.status = new_status
            self.save()
        return self.status

    def send_alert(self, old_status, new_status):
        send_mail(
            f'Cronjob {new_status} - {self}',
            f'Status changed from {old_status} to {new_status}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.ALERT_RECIPIENTS
        )


class Execution(models.Model):

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    start = models.DateTimeField()
    notification = models.DateTimeField(null=True)
    elapsed = models.BigIntegerField()
    exit_code = models.IntegerField()

    def success(self):
        return self.exit_code == 0
