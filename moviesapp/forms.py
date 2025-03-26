from django import forms
from .models import MovieRecommendation, Tag, Movie

class RecommendationForm(forms.ModelForm):
    class Meta:
        model = MovieRecommendation
        fields = ['movie', 'content', 'audience', 'mood', 'cherry', 'tag']

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'synopsis','release_year', 'genre', 'director', 'cover']