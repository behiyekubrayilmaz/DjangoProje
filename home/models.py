from django.db import models

# Create your models here.


class Setting(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = models.CharField(blank=True,max_length=150)
    phone = models.CharField(blank=True,max_length=15)
    fax = models.CharField(blank=True,max_length=150)
    email = models.CharField(blank=True,max_length=150)
    smtpserver = models.CharField(max_length=20)
    smtpemail = models.CharField(max_length=20)
    smtppassword = models.CharField(max_length=10)
    smtpport = models.CharField(blank=True,max_length=150)
    icon = models.ImageField(blank=True,upload_to='images/')
    instagram = models.CharField(max_length=150)
    twitter = models.CharField(max_length=150)
    facebook = models.CharField(max_length=150)
    aboutus = models.TextField()
    contact = models.TextField(blank=True)
    references = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
