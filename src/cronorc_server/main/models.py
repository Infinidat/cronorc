from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from djchoices import DjangoChoices, ChoiceItem
from urllib.parse import urljoin


class JobStatus(DjangoChoices):

    OK       = ChoiceItem()
    DELAYED  = ChoiceItem()
    FLAPPING = ChoiceItem()
    FAILED   = ChoiceItem()


class Job(models.Model):

    hostname          = models.CharField(max_length=255, db_index=True)
    ip                = models.GenericIPAddressField()
    command           = models.TextField(db_index=True)
    status            = models.CharField(max_length=10, db_index=True, choices=JobStatus.choices, default=JobStatus.OK)
    last_execution    = models.DateTimeField(null=True)
    last_notification = models.DateTimeField(null=True)
    display_name      = models.CharField(max_length=100, blank=True, null=True)
    period            = models.PositiveIntegerField(blank=True, null=True) # minutes

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

    def update_status(self, with_alert=True):
        new_status = self.status
        executions = self.execution_set.order_by('-id')[:5]
        if executions[0].success():
            new_status = JobStatus.OK
        else:
            new_status = JobStatus.FAILED
        # TODO identify flapping and delayed jobs
        if new_status != self.status:
            if with_alert:
                self.send_alert(self.status, new_status)
            self.status = new_status
            self.save()
        self.update_period(executions)
        return self.status

    def send_alert(self, old_status, new_status):
        url = urljoin(settings.CRONORC_URL, self.get_absolute_url())
        send_mail(
            f'Cronjob {new_status} - {self}',
            f'Status changed from {old_status} to {new_status}.\n\n{url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.ALERT_RECIPIENTS
        )

    def update_period(self, executions):
        period = self.identify_period(executions)
        if period and period != self.period:
            self.period = period
            self.save()

    def identify_period(self, executions):
        if len(executions) < 5:
            return None
        candidates = set()
        prev = None
        for curr in executions:
            if prev:
                candidate = (prev.start - curr.start).total_seconds() // 60
                candidates.add(candidate)
            prev = curr
        if len(candidates) == 1:
            return candidates.pop()
        return None

    def get_period_display(self):

        def _format(n, unit):
            return f'{n} {unit}s' if n > 1 else f'{n} {unit}'

        if self.period is None:
            return 'unknown'
        if self.period % 1440 == 0:
            return _format(self.period // 1440, 'day')
        if self.period % 60 == 0:
            return _format(self.period // 60, 'hour')
        return _format(self.period, 'minute')


class Execution(models.Model):

    job          = models.ForeignKey(Job, on_delete=models.CASCADE)
    start        = models.DateTimeField()
    notification = models.DateTimeField(null=True)
    elapsed      = models.BigIntegerField()
    exit_code    = models.IntegerField()

    def success(self):
        return self.exit_code == 0
