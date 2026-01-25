from django.db import models

# Create your models here.
class DemoAccountCreds(models.Model):
    enabled = models.BooleanField(default=False)
    username = models.CharField(default="demo")
    password = models.CharField(default="demo")
    
    def __str__(self):
        if not self.enabled:
            return "DISABLED."
        return f"(Enabled) {self.username}:{self.password}"