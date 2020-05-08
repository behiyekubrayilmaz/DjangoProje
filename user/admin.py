from django.contrib import admin

# Register your models here.
from user.models import AddActivity


class AddActivityAdmin(admin.ModelAdmin):
    list_display = ['user','title','name','surname','status']
    list_filter = ['status']

admin.site.register(AddActivity,AddActivityAdmin)