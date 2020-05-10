from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Menu(MPTTModel):
    STATUS =(
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=30, unique=True)
    status=models.CharField(max_length=10,choices=STATUS)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)  #self denildiği zaman kendi id si
    link = models.CharField(max_length=10, blank=True)
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

class Content(models.Model):
    TYPE = (
        ('menu', 'menu'),
        ('haber', 'haber'),
        ('duyuru', 'duyuru'),
        ('etkinlik', 'etkinlik'),
    )
    STATUS =(
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    menu=models.OneToOneField(Menu,null=True,blank=True,on_delete=models.CASCADE)  #category olduğunda category_id si
    type = models.CharField(max_length=20, choices=TYPE)
    title = models.CharField(max_length=150)
    keywords = models.CharField(blank=True,max_length=255)
    description = models.CharField(blank=True,max_length=255)
    image=models.ImageField(upload_to='images/')
    status=models.CharField(max_length=10,choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    detail=RichTextUploadingField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail',kwargs={'slug':self.slug})

class CImages(models.Model):
    content=models.ForeignKey(Content,on_delete=models.CASCADE)  #baglı olduğu activite silindiğinde burada da silinmesi için
    title = models.CharField(max_length=80, blank=True)
    image=models.ImageField(blank=True,upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'