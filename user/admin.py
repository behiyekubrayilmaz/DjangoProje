from django.contrib import admin

# Register your models here.
from user.models import AddActivity


class AddActivityAdmin(admin.ModelAdmin):
    list_display = ['user','title','name','surname','image_tag','status','detail']
    readonly_fields = ('image_tag',)
    list_filter = ['status']

admin.site.register(AddActivity,AddActivityAdmin)