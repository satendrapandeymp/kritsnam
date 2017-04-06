from django.db import models
import datetime
from django.contrib.auth.models import Permission, User
from django.core.urlresolvers import reverse
from django.forms import ModelForm
import time
from django_unixdatetimefield import UnixDateTimeField

class Gateway(models.Model):

    device_id = models.CharField(max_length = 32, unique=True)
    name = models.CharField(max_length = 32)
    description = models.TextField(max_length = 196, blank=True)
    doc = models.DateTimeField(default=datetime.datetime.now)

    def get_absolute_url(self):
        return reverse('czo:index')

    def __str__(self):
        return self.name

# for Node --
class Node(models.Model):

    name = models.CharField(max_length = 32)
    gateway_name = models.ForeignKey(Gateway,on_delete = models.CASCADE)
    owner = models.ForeignKey(User,on_delete = models.CASCADE)
    description = models.TextField(blank=True)
    doc = models.DateTimeField(default=datetime.datetime.now)

    def get_absolute_url(self):
        return reverse('czo:index')

    def __str__(self):
        return self.name

class GatewayStats(models.Model):

    gateway = models.ForeignKey(Gateway,on_delete = models.CASCADE)
    free_memory = models.IntegerField(help_text="Free memory")
    vcell = models.FloatField(help_text="battery voltage")
    soc = models.FloatField(help_text="state of charge")
    rssi = models.IntegerField(help_text="rssi value")
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        ordering = ['-timestamp']

class NodeStats(models.Model):

    node = models.ForeignKey(Node, on_delete = models.CASCADE)
    data = models.FloatField()
    rssi = models.IntegerField(help_text="rssi value")
    battery = models.FloatField(help_text="battery voltage")
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        ordering = ['-timestamp']

    def get_absolute_url(self):
        return reverse('czo:index')

    def __str__(self):
        return str(self.data)
