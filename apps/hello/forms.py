# -- coding: utf-8 --
from django.forms import ModelForm
from .models import AboutMe
from django import forms


class ProfileUpdateForm(ModelForm):
    ''' ModelForm maps AboutMe Model to a Form '''

    class Meta:
        model = AboutMe
        fields = [
            'first_name',
            'last_name',
            'birthday',
            'email',
            'jabber',
            'skype',
            'contacts',
            'bio',
            'photo'
        ]
