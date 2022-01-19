from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import UserCreationForm

from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields =   UserCreationForm.Meta.fields + ('location_state', "location_city", 'height', 'weight', 'age')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('location_state', "location_city", 'height', 'weight', 'age')