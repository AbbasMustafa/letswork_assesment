from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "location", "owner", "created_at")
    search_fields = ("title", "description", "location", "owner__username")
    list_filter = ("date", "location", "created_at")
    ordering = ("-date",)
    filter_horizontal = ("attendees",)
