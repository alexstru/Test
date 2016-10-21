# -- coding: utf-8 --
from django.forms import ModelForm
from .models import AboutMe
from django import forms
from widgets import DatePickerWidget


class ProfileUpdateForm(ModelForm):
    ''' ModelForm maps AboutMe Model to a Form '''

    class Meta:
        model = AboutMe
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form_widget'}),
            'last_name': forms.TextInput(attrs={'class': 'form_widget'}),
            'email': forms.TextInput(attrs={'class': 'form_widget'}),
            'jabber': forms.TextInput(attrs={'class': 'form_widget'}),
            'skype': forms.TextInput(attrs={'class': 'form_widget'}),
            'contacts': forms.Textarea(attrs={'class': 'form_widget'}),
            'bio': forms.Textarea(attrs={'class': 'form_widget'}),
        }

    birthday = forms.DateField(widget=DatePickerWidget(
        params="dateFormat: 'yy-mm-dd',\
                changeYear: true,\
                yearRange: 'c-115:c'",
        attrs={'class': 'datepicker form_widget'}
        )
      )
