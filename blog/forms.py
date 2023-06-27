from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
from .models import Post, UserProfile
from ckeditor.widgets import CKEditorWidget


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


class UserProfileForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input'}))
    username = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['profile_image', 'gender', 'bio', 'website',
                  'phone', 'location', 'date_of_birth', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
