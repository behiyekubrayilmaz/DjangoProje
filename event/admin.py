from django.contrib import admin

# Register your models here.
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from event.models import Category, Event, Images, Comment


class EventImageInline(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','status']
    readonly_fields = ('image_tag',)
    list_filter = ['status']

class EventAdmin(admin.ModelAdmin):
    list_display = ['title','category','image_tag','status']
    readonly_fields = ('image_tag',)
    list_filter = ['status','category']
    inlines = [EventImageInline]
    prepopulated_fields = {'slug': ('title',)}

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','event','image_tag']
    readonly_fields = ('image_tag',)

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_events_count', 'related_events_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug':('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Event,
                'category',
                'events_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Event,
                 'category',
                 'events_count',
                 cumulative=False)
        return qs

    def related_events_count(self, instance):
        return instance.events_count

    related_events_count.short_description = 'Related events (for this specific category)'

    def related_events_cumulative_count(self, instance):
        return instance.events_cumulative_count
    related_events_cumulative_count.short_description = 'Related events (in tree)'

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'event', 'user', 'status']
    list_filter = ['status']

admin.site.register(Category,CategoryAdmin2)
#admin.site.register(Event)
admin.site.register(Event,EventAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(Comment,CommentAdmin)