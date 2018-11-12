from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class TodoUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')
