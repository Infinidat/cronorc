from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone

import json

from .models import Job, Execution


@require_POST
@csrf_exempt
def notify_view(request):
    message = json.loads(request.body)
    print(message)
    job, _ = Job.objects.update_or_create(
        hostname=message['hostname'],
        ip=message['ip'],
        command=message['command'],
        defaults=dict(
            last_execution=message['start'],
            last_notification=timezone.now()
        )
    )
    Execution.objects.create(
        job=job,
        start=message['start'],
        elapsed=message['elapsed'],
        exit_code=message['exitcode'],
        notification=timezone.now()
    )
    job.update_status()
    return HttpResponse('{}', content_type='application/json')


@login_required
def home_view(request):
    executions = Execution.objects.order_by('-id')
    jobs = Job.objects.order_by('-last_execution')
    return render(request, 'home.html', locals())


@login_required
def job_view(request, id):
    job = get_object_or_404(Job, id=id)
    executions = job.execution_set.order_by('-id')
    return render(request, 'job.html', locals())
