from django import forms

from captcha.fields import ReCaptchaField, ReCaptchaV3

from .models import Ticket


class TicketForm(forms.ModelForm):
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
