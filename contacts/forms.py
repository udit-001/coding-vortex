from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from django import forms
from django.conf import settings

from .models import Contact


class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField(public_key=settings.RECAPTCHA_PUBLIC_KEY,
                             private_key=settings.RECAPTCHA_PRIVATE_KEY, widget=ReCaptchaV2Invisible)

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
