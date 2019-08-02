from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
    )

    def clean_confirm_password(self):
        if self.data['confirm_password'] != self.data['password']:
            raise ValidationError('Пароли не совпадают.')
        return self.data['confirm_password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

    class Meta:
        fields = ('email', 'username')
        model = get_user_model()
