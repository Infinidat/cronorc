from django.contrib import admin

from .models import Job, Execution

class ExecutionAdmin(admin.ModelAdmin):

    list_display = ('job', 'start', 'elapsed', 'exit_code')


admin.site.register(Job)
admin.site.register(Execution, ExecutionAdmin)
