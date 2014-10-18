from django.contrib import admin
from lyrics.models import Song


class SongAdmin(admin.ModelAdmin):
    list_display = ['aid', 'artist', 'title', 'duration', 'url']


admin.site.register(Song, SongAdmin)
