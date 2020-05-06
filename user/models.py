from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm
from django.utils.safestring import mark_safe

from event.models import Category


class AddActivity(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # category olduğunda category_id si
    title = models.CharField(max_length=150)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    #image = models.ImageField(blank=True, upload_to='images/')
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    detail = RichTextUploadingField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class AddActivityForm(ModelForm):
    class Meta:
        model = AddActivity
        fields = ['title','status','detail']