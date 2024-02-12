from django.contrib import admin

from storage.models import File


class FileAdmin(admin.ModelAdmin):
    readonly_fields = File.readonly_fields

admin.site.register(File, FileAdmin)
