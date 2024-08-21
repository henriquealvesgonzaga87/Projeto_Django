from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name',
            'username',
            'email',
            'password'
            ]
        
        labels = {
            'username': "Username",
            "first_name": "First name",
            "last_name": "Last name",
            "email": "E-mail",
            "password": "Password"
        }

        help_texts = {
            "email": "example@example.com"
        }

        error_messages = {
            "username": {
                "required": "This field can't be empty",
            }
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': "Type your username"
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': "Type your password here"
            })
        }
