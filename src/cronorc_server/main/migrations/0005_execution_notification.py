# Generated by Django 2.2.9 on 2020-01-26 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_job_last_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='execution',
            name='notification',
            field=models.DateTimeField(null=True),
        ),
    ]
