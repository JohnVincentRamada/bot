from django import forms
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from captcha.fields import CaptchaField
from django.contrib.auth import get_user_model

class CaptchaForm(forms.Form):
    captcha = CaptchaField()

class SetPasswordForm(SetPasswordForm):
   class Meta:
    model = get_user_model()
    fields = [
        'new_passord1',
        'new_password2'
    ]

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        