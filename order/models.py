from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm

from event.models import Event


class ActivityPage(models.Model):

    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    quantity= models.IntegerField()

    def __str__(self):
        return self.event

class ActivityPageForm(ModelForm):
    class Meta:
        model =ActivityPage
        fields = ['quantity']