from django.contrib import admin

from user.models import LockboxUser


class LockboxUserAdmin(admin.ModelAdmin):
    readonly_fields = LockboxUser.readonly_fields

admin.site.register(LockboxUser, LockboxUserAdmin)
