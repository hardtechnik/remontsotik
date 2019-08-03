from django import forms

from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        fields = (
            'phone_model',
            'malfunction',
            'phone_number',
            'address',
        )
        model = Ticket
