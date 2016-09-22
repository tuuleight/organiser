from django import forms
from .models import Event
from django.contrib.auth.models import User


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = (
            'date_start', 'date_duration',
            'name', 'text', 'private',
            )


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', )
