from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile, CustomUser


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_organiser', 'password1', 'password2']


class UserUpdateForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_organiser']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']