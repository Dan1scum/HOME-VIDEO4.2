from django import forms
from .models import Movie, UserProfile
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
            if poster.content_type and not poster.content_type.startswith('image'):
                raise forms.ValidationError('Please upload a valid image file')
        return poster


class MovieEditForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'poster', 'category', 'genres', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'poster': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'genres': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10', 'step': '0.1'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if len(title) < 2:
            raise forms.ValidationError('Title must be at least 2 characters long')
        return title

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None:
            if rating < 0 or rating > 10:
                raise forms.ValidationError('Rating must be between 0 and 10')
        return rating


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'birth_date', 'phone']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell about yourself', 'maxlength': '500'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 000-00-00'}),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 2 * 1024 * 1024:  # 2MB limit
                raise forms.ValidationError('Avatar size must not exceed 2MB')
            if avatar.content_type and not avatar.content_type.startswith('image'):
                raise forms.ValidationError('Please upload a valid image file')
        return avatar

    def clean_bio(self):
        bio = self.cleaned_data.get('bio', '')
        if len(bio) > 500:
            raise forms.ValidationError('Bio must not exceed 500 characters')
        return bio


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters long')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken')
        return username

