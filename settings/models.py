from django.db import models
from django.contrib.auth.models import User


class LMS(models.Model):
    Name = models.CharField(max_length=100)
    PointsIsOn = models.BooleanField(default=False)
    MaxPoints = models.IntegerField(default=0)


class LMSUsers(models.Model):
    lms = models.ForeignKey(LMS, on_delete= models.CASCADE)
    user = models.ForeignKey(User, unique=True, on_delete= models.CASCADE)

