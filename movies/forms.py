from django import forms
from .models import Movie
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'poster', 'category', 'genres']

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if len(title) < 2:
            raise forms.ValidationError('Title must be at least 2 characters long')
        return title


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use')
        return email
