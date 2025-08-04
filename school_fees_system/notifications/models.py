from django.db import models
from accounts.models import CustomUser
# Create your models here.
class Notification(models.Model):
    parent = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.parent.email} - {self.title}"
