from django.contrib import admin
from .models import UserFile


@admin.register(UserFile)
class UserFileAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'file',
        'uploaded_at',
    )

    list_filter = (
        'uploaded_at',
        'user',
    )

    search_fields = (
        'file',
        'user__username',
        'user__email',
    )

    ordering = (
        '-uploaded_at',
    )