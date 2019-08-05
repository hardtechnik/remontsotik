from django.contrib import admin
from django.utils.safestring import mark_safe

from .s3 import get_presigned_url
from .models import Ticket, Image, Status


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0
    fields = ('image',)
    readonly_fields = ('image',)

    def has_add_permission(self, request, obj=None):
        return False

    @staticmethod
    def image(obj):
        if obj.url:
            url = get_presigned_url(obj.url, expires_in=10)
            return mark_safe(f'<img src="{url}" width="600" height=auto>')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    search_fields = ('number', 'name')
    list_filter = ('status__name',)
    readonly_fields = ('number',)
    list_display = (
        'number',
        'status',
        'name',
        'phone_number',
        'email',
        'created',
    )
    date_hierarchy = 'created'
    inlines = (ImageInline, )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('status')
