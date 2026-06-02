from django.contrib import admin

# Register your models here.

from .models import Video


@admin.register(Video)
class MovieAdmin(admin.ModelAdmin):
    fields = ["name", "owner", "is_published", "created_at", "total_likes"]

    readonly_fields = ["created_at", "total_likes"]

    list_display = ("id", "name", "owner", "total_likes", "is_published")
    list_display_links = ("id", "name")

    ordering = ["-is_published", "-total_likes", "name"]
    list_per_page = 20

    search_fields = [
        "name",
        "owner__username",
    ]

    list_filter = ["is_published", "created_at"]

    save_on_top = True

    actions = ["make_published", "make_unpublished"]

    @admin.action(description="Опубликовать выбранные видео")
    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Снять с публикации выбранные видео")
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)
