from django.db import models
from django.contrib.auth import get_user_model
from datetime import date
User = get_user_model()

# Create your models here.

class ScheduleSlot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    DAY_CHOICES = {
        "mon": "Monday",
        "tue": "Tuesday",
        "wed": "Wednesday",
        "thu": "Thursday",
        "fri": "Friday",
        "sat": "Saturday",
        "sun": "Sunday"
    }
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    period = models.PositiveIntegerField()
    subject = models.CharField(max_length=200, default="[placeholder]")

    def get_display(self):
        return self.subject
    
    def __str__(self):
        return f"{self.day} {self.period}: {self.subject}"
    
    class Meta:
        unique_together = ['user', 'day', 'period']

class PendingWork(models.Model):
    created = models.DateField(auto_now_add=True)
    due = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000, blank=True)
    completed = models.BooleanField(default=False)
    
    def time_left(self):
        return self.due - date.today()