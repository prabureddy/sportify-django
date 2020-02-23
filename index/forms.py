from django import forms
from django.core import validators
from index.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Contactform(forms.ModelForm):

    class Meta:
        model = Contact
        exclude = ('date',)
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Full Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Email','type': 'email'}),
            'message': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Message'}),
        }

    confirm_email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Confirm Email','type': 'email'}))
    botcatcher = forms.CharField(required=False,
                                    widget=forms.HiddenInput,
                                    validators=[validators.MaxLengthValidator(0)])

    def clean(self):
        super(Contactform, self).clean()
        email = self.cleaned_data['email']
        cemail = self.cleaned_data['confirm_email']
        if email != cemail:
            raise forms.ValidationError("MAKE SURE EMAIL MATCH!!!")



class Feedbackform(forms.ModelForm):

    class Meta:
        model = Contact
        exclude = ('date',)
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Full Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Email','type': 'email'}),
            'message': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Message'}),
        }

    confirm_email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Confirm Email','type': 'email'}))
    botcatcher = forms.CharField(required=False,
                                    widget=forms.HiddenInput,
                                    validators=[validators.MaxLengthValidator(0)])

    def clean(self):
        super(Feedbackform, self).clean()
        email = self.cleaned_data['email']
        cemail = self.cleaned_data['confirm_email']
        if email != cemail:
            raise forms.ValidationError("MAKE SURE EMAIL MATCH!!!")
