from django import forms
from django.conf import settings

from captcha.fields import ReCaptchaField, ReCaptchaV3

from .models import Ticket


class TicketForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3(api_params={
        'hl': 'ru',
    }))

    def clean(self):
        cleaned_data = super().clean()
        if settings.CI:
            self.errors.pop('captcha', None)
        return cleaned_data

    class Meta:
        exclude = (
            'id',
            'number',
            'status',
        )
        model = Ticket
