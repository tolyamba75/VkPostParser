from django.contrib import admin

# Register your models here.
from .models import Task, Recipient, ProcessingGroup, AccessToken

admin.site.register(Task)
admin.site.register(Recipient)
admin.site.register(ProcessingGroup)
admin.site.register(AccessToken)
