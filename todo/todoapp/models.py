from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name
