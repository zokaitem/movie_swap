from django import forms
from django.contrib.auth.models import User
from .models import MovieRecommendation, Tag, Movie, Profile

class RecommendationForm(forms.ModelForm):
    class Meta:
        model = MovieRecommendation
        fields = ['movie', 'content', 'audience', 'mood', 'cherry', 'tag']

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'synopsis','release_year', 'genre', 'director', 'cover']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']