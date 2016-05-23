import datetime

from django.db import models
from django.utils import timezone


# Create your models here.
class Friend(models.Model):

    name = models.CharField(max_length=30, default='username')
    mid = models.CharField(max_length=40, primary_key=True)
    is_block = models.BooleanField(default=False)
    edit_time = models.DateTimeField('上次修改時間', auto_now=True, editable=False)

    def __str__(self):
        return '%s(%s)' % (self.name, self.mid)

    def was_edited_recently(self, days=1):
        return self.edit_time >= timezone.now() - datetime.timedelta(days=days)

class Question(models.Model):

    text = models.CharField(max_length=90)
    friend_id = models.CharField(max_length=40)
    edit_time = models.DateTimeField('上次修改時間', auto_now=True, editable=False)

    def was_edited_recently(self, seconds=60*5):
        return self.edit_time >= timezone.now() - datetime.timedelta(seconds=seconds)
