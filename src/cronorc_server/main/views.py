from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import json

from .models import Job, Execution


@require_POST
@csrf_exempt
def notify_view(request):
    message = json.loads(request.body)
    print(message)
    job, _ = Job.objects.get_or_create(
        hostname=message['hostname'],
        ip=message['ip'],
        command=message['command']
    )
    Execution.objects.create(
        job=job,
        start=message['start'],
        elapsed=message['elapsed'],
        exit_code=message['exitcode']
    )
    return HttpResponse('{}', content_type='application/json')


@login_required
def home_view(request):
    executions = Execution.objects.order_by('-id')
    return render(request, 'home.html', locals())
