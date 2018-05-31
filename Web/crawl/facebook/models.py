'''
from django.db import models
from mongoengine import connect, Document, StringField,DateTimeField
import os
import datetime

uri = os.getenv('MLAB_URI')
connect(host=uri)
'''
# Create your models here.

