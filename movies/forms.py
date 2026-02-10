from django import forms
from .models import Movie
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'poster', 'category', 'genres']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'poster': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'genres': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if len(title) < 2:
            raise forms.ValidationError('Title must be at least 2 characters long')
        if len(title) > 200:
            raise forms.ValidationError('Title must not exceed 200 characters')
        return title
    
    def clean_release_date(self):
        release_date = self.cleaned_data.get('release_date')
        if release_date and release_date > date.today():
            raise forms.ValidationError('Release date cannot be in the future')
        return release_date
    
    def clean_poster(self):
        poster = self.cleaned_data.get('poster')
        if poster:
            if poster.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('Image size must not exceed 5MB')
            if not poster.content_type.startswith('image'):
                raise forms.ValidationError('Please upload a valid image file')
        return poster


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
