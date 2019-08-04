from django import forms

from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        exclude = (
            'id',
            'number',
            'status',
        )
        model = Ticket
