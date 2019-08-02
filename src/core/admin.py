from django.contrib import admin

from .models import Malfunction, Phone, Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    pass


@admin.register(Malfunction)
class MalfunctionAdmin(admin.ModelAdmin):
    pass
