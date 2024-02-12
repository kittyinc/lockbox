from django.contrib import admin

from common.models import Configuration


class LockboxModelAdmin(admin.ModelAdmin):
    readonly_fields = Configuration.readonly_fields


admin.site.register(Configuration, LockboxModelAdmin)
