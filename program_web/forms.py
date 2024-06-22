from django import forms
from django.forms import ModelForm
from .models import MyUser


class SearchForm(forms.Form):
    query = forms.CharField(label='', max_length=150, required=False)

class SignupForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'password', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Сonfirm Password'})

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

