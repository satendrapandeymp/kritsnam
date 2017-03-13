from django.db import models
import datetime
from django.contrib.auth.models import Permission, User
from django.core.urlresolvers import reverse
from django.forms import ModelForm
import time
from itertools import chain
from django_unixdatetimefield import UnixDateTimeField


class Profile(models.Model):
    first_name = models.CharField(max_length = 40)
    last_name = models.CharField(max_length = 40)
    owner = models.ForeignKey(User,on_delete = models.CASCADE)
    about = models.TextField(max_length = 400, blank=True)
    doc = models.FloatField(max_length = 16,blank=True )
    image = models.FileField()
    def get_absolute_url(self):
        return reverse('chain:index')
    def __str__(self):
        return self.first_name

# for Node --
class Node(models.Model):
    name = models.CharField(max_length = 40)
    owner = models.ForeignKey(User,on_delete = models.CASCADE)
    description = models.TextField(max_length = 400, blank=True)
    doc = models.DateTimeField(blank=True, default=datetime.datetime.now)
    def get_absolute_url(self):
        return reverse('chain:index')
    def __str__(self):
    #    str1 = str(self.owner) + ' -- ' + self.name
        return self.name

# For Sensor --
class Sensor(models.Model):
    node_name = models.ForeignKey(Node,on_delete = models.CASCADE)
    name = models.CharField(max_length = 40)
    description = models.TextField(max_length = 400, blank=True)
    doc = models.DateTimeField(blank=True, default=datetime.datetime.now)
    def get_absolute_url(self):
        return reverse('chain:index')
    def __str__(self):
        return str(self.name)

# For Data --
class Data(models.Model):
    sensor_name = models.ForeignKey(Sensor,on_delete = models.CASCADE)
    data = models.FloatField(default = 1.000)
    doc = models.DateTimeField(blank=True, default=datetime.datetime.now)
    class Meta:
        ordering = ['-doc']
    def get_absolute_url(self):
        return reverse('chain:index')
    def __str__(self):
        return str(self.sensor_name)


# For Node Form
class NodeForm(ModelForm):
    class Meta:
        model = Node
        exclude = ('owner', 'doc',)

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('owner', 'doc',)

# For Sensor to set that in form you can get only User nodes.
class SensorForm(ModelForm):
    class Meta:
        model = Sensor
        exclude = ('doc',)
    def __init__(self, var=None, *args, **kwargs):
        super(SensorForm, self).__init__(*args, **kwargs)
        self.fields['node_name'].queryset = Node.objects.filter(owner=var)
