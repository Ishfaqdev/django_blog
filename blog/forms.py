from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
from .models import Post
from ckeditor.widgets import CKEditorWidget
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        error_messages={
            'required': 'Please enter your password.'},
        widget=forms.PasswordInput(attrs={
            'class': 'form-control my-class',
            'placeholder': 'Password'
        }),
    )
    password2 = forms.CharField(
        label='Confirm Password',
        error_messages={
            'required': 'Please confirm your password.'},
        widget=forms.PasswordInput(attrs={
            'class': 'form-control my-class',
            'placeholder': 'Confirm Password'
        }),
    )

    def clean_username(self):
        username = self.cleaned_data['username']

        # Check if the username contains only numbers
        if username.isdigit():
            raise ValidationError('Username cannot contain only numbers.')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if not email:
            raise ValidationError('Please enter your email.')

        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'email': 'Email'
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control my-class',
                'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control my-class',
                'placeholder': 'Email'
            })}
        error_messages = {
            'username': {
                'required': 'Please enter your username.',
                'invalid': 'Please enter a valid username! Use "-" or "_" instead of spaces',
            },
            'email': {
                'required': 'Please enter your email.',
            },
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(
        error_messages={
            'required': 'Please enter your username.',
            'invalid': 'Please enter a valid username! ',
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control my-class',
            'placeholder': 'Full Name'
        }),

    )
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={
                                   'class': 'form-control my-class',
                                   'placeholder': 'Password'
                                   }),
        error_messages={
            'required': 'Please enter your password.',
            'invalid': 'Please enter a valid password.',
        }
    )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8, 'placeholder':
                'Enter post content'}),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'}),
            'category': forms.Select(attrs={
                'class': 'form-control'}),
        }
