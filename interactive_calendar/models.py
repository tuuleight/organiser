from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


class Event(models.Model):
    author = models.CharField(max_length=100)
    date_start = models.DateTimeField(default=timezone.now)
    date_duration = models.DurationField(default=0)
    name = models.CharField(max_length=200)
    text = models.TextField()  # to describe the event
    attenders_num = models.IntegerField(default=0)
    attenders = ArrayField(
        models.CharField(max_length=100, blank=True, null=True),
        null=True
    )
    invited = ArrayField(
        models.CharField(max_length=100, blank=True, null=True),
        null=True
    )
    private = models.BooleanField()  # if private, only invited persons can see
    #  the event

    def __str__(self):
        return self.name
