from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    captcha = ReCaptchaField(public_key=settings.RECAPTCHA_PUBLIC_KEY,
                             private_key=settings.RECAPTCHA_PRIVATE_KEY, widget=ReCaptchaV2Invisible)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
