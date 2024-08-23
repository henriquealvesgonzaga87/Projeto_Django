from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your email')
        add_placeholder(self.fields['first_name'], 'Ex: John')
        add_placeholder(self.fields['last_name'], 'Ex: Doe')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')

    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        required=True,
        label='First name'
    )

    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        required=True,
        label='Last name'
    )

    username = forms.CharField(
        error_messages={
            'required': "This field can't be empty",
            'min_lenght': "Username must have at least 4 and 150 characters",
            'max_lenght': 'Username must have less than 150 characters'
            },
        required=True,
        label='Username',
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        min_length=4,
        max_length=150
    )

    email = forms.EmailField(
        error_messages={'required': "Email is not valid"},
        required=True,
        label='E-mail',
        help_text='example@example.com'
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={"required": "This field can't be empty"},
        help_text="Must have at least one uppercase and one uppercase letter and one number",
        validators=[strong_password],
        label="Password"
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={"required": "This field can't be empty"},
        help_text="You need to repeat your password",
        label="Password"
    )


    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name',
            'username',
            'email',
            'password'
            ]
        
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError('User e-mail is already in use', code='invalid',)

        return email
    
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                    "The passwords don't match",
                    code='Invalid'
                )
            raise ValidationError({
                "password": password_confirmation_error,
                "password2": [
                    password_confirmation_error
                ]
            })
