from django import forms
from customadmin.models import Description
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class DescriptionForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = ['title', 'category', 'answer']
        widgets = {
                'answer': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }
    def __init__(self, *args, **kwargs):
        super(DescriptionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
