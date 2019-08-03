from django.contrib import admin

from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    search_fields = ('number', 'name')
    list_filter = ('status',)
    list_display = ('number', 'status', 'name', 'phone_number', 'created')
    date_hierarchy = 'created'
