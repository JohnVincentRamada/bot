from django import forms
from bot.models import Log
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class LogForm(ModelForm):
    class Meta:
        model = Log
        fields = [
            'bot',
            'question',
            'user',
        ]
    def __init__(self, *args, **kwargs):
        super(LogForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
