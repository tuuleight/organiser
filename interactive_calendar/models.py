from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


class Event(models.Model):
    author = models.ForeignKey('auth.User')
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

    def __repr__(self):
        return 'Event %r created by %r' % (self.name, self.author)

    def add_attenders_num(self):
        self.attenders_num += 1

    def del_attenders_num(self):
        self.attenders_num -= 1

    def add_attenders(self, name):
        try:
            self.attenders.append(name)
            self.attenders = [i for i in self.attenders
                              if self.attenders.count(i) < 2]
        except AttributeError:
            self.attenders = [name]

        if name in self.invited:
            self.invited.remove(name)

    def del_attenders(self, name):
        """ 'don't attend' button is displayed for current user only after
        joining to the event first, so no AttributeError handler needed"""
        self.attenders.remove(name)

    def update_invited(self, name):
        try:
            self.invited.append(name)
            self.invited = [i for i in self.invited
                            if self.invited.count(i) < 2]
        except AttributeError:
            self.invited = [name]
