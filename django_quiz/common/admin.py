# Django
from django.contrib import admin

# Local
from .models import Tag

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')

admin.site.register(Tag, TagAdmin)
