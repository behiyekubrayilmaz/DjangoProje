from django.contrib import admin

# Register your models here.
from event.models import Category, Event, Images

class EventImageInline(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','status']
    readonly_fields = ('image_tag',)
    list_filter = ['status']

class EventAdmin(admin.ModelAdmin):
    list_display = ['title','category','detail','image_tag','status']
    readonly_fields = ('image_tag',)
    list_filter = ['status','category']
    inlines = [EventImageInline]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','event','image_tag']
    readonly_fields = ('image_tag',)

admin.site.register(Category,CategoryAdmin)
#admin.site.register(Event)
admin.site.register(Event,EventAdmin)
admin.site.register(Images,ImagesAdmin)