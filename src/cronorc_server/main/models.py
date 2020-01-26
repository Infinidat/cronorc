from django.db import models

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

    class Meta:
        unique_together = ('hostname', 'ip', 'command')

    def __str__(self):
        cmd = self.command[:100] + '...' if len(self.command) > 100 else self.command
        return f'{self.hostname} [{self.ip}] {cmd}'

    def update_status(self):
        new_status = self.status
        executions = self.execution_set.order_by('-id')[:5]
        if executions[0].success():
            new_status = JobStatus.OK
        else:
            new_status = JobStatus.FAILED
        # TODO identify flapping and delayed jobs
        if new_status != self.status:
            self.status = new_status
            self.save()
        return self.status


class Execution(models.Model):

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    start = models.DateTimeField()
    notification = models.DateTimeField(null=True)
    elapsed = models.BigIntegerField()
    exit_code = models.IntegerField()

    def success(self):
        return self.exit_code == 0
