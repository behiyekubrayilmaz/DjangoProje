from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput, Select, FileInput
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS =(
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=10,choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)  #self denildiği zaman kendi id si
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_inserttion_by =['title']

    def __str__(self):
        full_path= [self.title]
        k= self.parent
        while k is not None:
            full_path.append(k.title)
            k=k.parent
        return ' -> '.join(full_path[::-1])

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail',kwargs={'slug':self.slug})

class Event(models.Model):
    STATUS =(
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)  #category olduğunda category_id si
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    slug = models.SlugField(null=False, unique=True)
    status=models.CharField(max_length=10,choices=STATUS)
    detail=RichTextUploadingField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail',kwargs={'slug': self.slug})

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['category','title','slug','keywords','description','image','detail']
        widgets = {
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'title'}),
            'slug': TextInput(attrs={'class': 'input', 'placeholder': 'slug'}),
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'keywords'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
            'category': Select(attrs={'class': 'input', 'placeholder': 'city'},choices=Category.objects.all()),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
            'detail': CKEditorWidget(),
        }

class Images(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE)  #baglı olduğu activite silindiğinde burada da silinmesi için
    title = models.CharField(max_length=80, blank=True)
    image=models.ImageField(blank=True,upload_to='images/')
    def __str__(self):
        return self.title
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class EventImageForm(ModelForm):
    class Meta:
        model = Images
        fields = ['title', 'image']


class Comment(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    event=models.ForeignKey(Event,on_delete=models.CASCADE) #baglı olduğu activite silindiğinde burada da silinmesi için
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=80, blank=True)
    comment = models.TextField(max_length=200, blank=True)
    rate = models.IntegerField(blank=True)
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(max_length=20, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields=['subject','comment','rate']


