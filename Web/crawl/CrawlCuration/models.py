'''
from django.db import models
from mongoengine import connect, Document, StringField,DateTimeField
import os
import datetime

uri = os.getenv('MLAB_URI')
connect(host=uri)
'''
# Create your models here.
from __future__ import unicode_literals

from django.db import models


class Bar(models.Model):
    word = models.CharField(max_length=100)
    freq = models.FloatField()
