from django import forms
from django.conf import settings

from captcha.fields import ReCaptchaField, ReCaptchaV3

from .models import Ticket


class TicketForm(forms.ModelForm):
    if not settings.CI:
        captcha = ReCaptchaField(widget=ReCaptchaV3(api_params={
            'hl': 'ru',
        }))

    class Meta:
        exclude = (
            'id',
            'number',
            'status',
        )
        model = Ticket
