from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Invitation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    message = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
