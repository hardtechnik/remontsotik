from django.contrib import admin

from .models import Ticket, Image, Status


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    search_fields = ('number', 'name')
    list_filter = ('status__name',)
    list_display = ('number', 'status', 'name', 'phone_number', 'created')
    date_hierarchy = 'created'
    inlines = (ImageInline, )
