from django.db import models
from django.contrib.auth.models import User


class LMS(models.Model):
    Name = models.CharField(max_length=100)
    PointsIsOn = models.BooleanField(default=False)
    MaxPoints = models.IntegerField(default=0, blank=True, null=True)
    MaxLevel = models.IntegerField(default=10, blank=True, null=True)
    PointPerLevel = models.IntegerField(default=0, blank=True, null=True)


class LMSUsers(models.Model):
    lms = models.ForeignKey(LMS, on_delete=models.CASCADE)
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)


class LMSEvents(models.Model):
    name = models.CharField(max_length=100)
    lms = models.ForeignKey(LMS, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('lms', 'name')

    def __str__(self):
        return self.name


class EventPoints(models.Model):
    event = models.ForeignKey(LMSEvents, on_delete=models.CASCADE)
    lms = models.ForeignKey(LMS, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    class Meta:
        unique_together = ('lms', 'event')


class LevelOptions(models.Model):
    event = models.ForeignKey(LMSEvents, on_delete=models.CASCADE)
    lms = models.ForeignKey(LMS, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    isActive = models.BooleanField(default=True)

    class Meta:
        unique_together = ('lms', 'event')


class Parameters(models.Model):
    name = models.CharField(max_length=50)
    event = models.ForeignKey(LMSEvents, on_delete=models.CASCADE, null=True)
    lms = models.ForeignKey(LMS, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Badges(models.Model):
    name = models.CharField(max_length=50)
    img = models.CharField(max_length=200)
    parameter = models.ForeignKey(Parameters, on_delete=models.CASCADE)
    comparison_type = models.IntegerField(default=0)
    criterion = models.IntegerField(default=0)
    lms = models.ForeignKey(LMS, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=True)
