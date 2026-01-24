from django.contrib import admin
from .models import ScheduleSlot, PendingWork

# Register your models here.
admin.site.register(ScheduleSlot)
admin.site.register(PendingWork)