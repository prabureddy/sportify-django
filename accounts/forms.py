from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import datetime
from django.forms import ModelForm



class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control','placeholder': 'Username',"name":"username","autofocus":"","type":"text","id":"id_username","required":""}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control','placeholder': 'Password',"name":"password","type":"password","required":"","id":"id_password",}))



class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'username','required':''}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name','required':''}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Last Name','required':''}),
            'email': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Email','type': 'email','required':''}),
            'password1': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Password','type': 'password','required':''}),
            'password2': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Confirm Password','type': 'password','required':''}),
        }

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'})


    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data["username"]).exists():
            raise forms.ValidationError("Username Already Exists!!!")
        return self.cleaned_data["username"]

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise forms.ValidationError("Email Already Exists!!!")
        return self.cleaned_data["email"]


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('registration_no','phone_no','passing_year',)
        widgets = {
            'phone_no': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Phone Number','type':'number'}),
            'registration_no': forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name','type':'number'}),
            'passing_year': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Last Name','type':'date'}),
        }

    def clean_registration_no(self):
        if UserProfile.objects.filter(registration_no=self.cleaned_data["registration_no"]).exists():
            raise forms.ValidationError("Registration No. Already Exists!!!")
        registration_no = self.cleaned_data["registration_no"]
        registration_no = len(str(registration_no))

        if registration_no == 8 or registration_no == 5:
            pass
        else:
            raise forms.ValidationError("Enter Correct Registration No.!!!")
        return self.cleaned_data["registration_no"]

    def clean_phone_no(self):

        phone_no = self.cleaned_data["phone_no"]
        phone_no_len = len(str(phone_no))

        if phone_no_len == 10:
            pass
        else:
            raise forms.ValidationError("Enter Correct Mobile No.!!!")

        return phone_no

    def clean_passing_year(self):

        passing_year = self.cleaned_data["passing_year"]
        now = datetime.date.today()

        if str(passing_year) > str(now.year):
            pass
        else:
            raise forms.ValidationError("Enter Correct Passing Year.!!!")

        return passing_year



# class EditProfileForm(UserChangeForm):
#     template_name='account/profile_update.html'
#
#     class Meta:
#         model = User
#         fields = ('first_name','last_name',)


class EditProfileForm(ModelForm):
    username = forms.CharField(disabled=True)
    email = forms.EmailField(disabled=True)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

class ProfileForm(ModelForm):
    phone_no = forms.IntegerField()
    registration_no = forms.IntegerField(disabled=True)

    class Meta:
         model = UserProfile
         fields = ('registration_no','phone_no')


    def clean_phone_no(self):

         phone_no = self.cleaned_data["phone_no"]
         phone_no_len = len(str(phone_no))

         if phone_no_len == 10:
             pass
         else:
             raise forms.ValidationError("Enter Correct Mobile No.!!!")

         return phone_no
