from django.db import models


class Job(models.Model):

    hostname = models.CharField(max_length=255, db_index=True)
    ip = models.GenericIPAddressField()
    command = models.TextField(db_index=True)

    class Meta:
        unique_together = ('hostname', 'ip', 'command')

    def __str__(self):
        cmd = self.command[:100] + '...' if len(self.command) > 100 else self.command
        return f'{self.hostname} [{self.ip}] {cmd}'


class Execution(models.Model):

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    start = models.DateTimeField()
    elapsed = models.BigIntegerField()
    exit_code = models.IntegerField()

    def success(self):
        return self.exit_code == 0
