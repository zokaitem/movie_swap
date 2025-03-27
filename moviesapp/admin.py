from django.contrib import admin
from .models import Movie, MovieRecommendation, Tag, Comment, Profile

class MovieRecommendationAdmin(admin.ModelAdmin):
    list_display = ['movie','year','tag','genre','user']
    list_editable = ['year','movie', 'genre']
    search_fields = ['movie','tag','genre','user']

class MovieAdmin(admin.ModelAdmin):
    list_display = ['title','year','genre','director']
    search_fields = ['title','year','genre','director']

admin.site.register(MovieRecommendation)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Movie)
admin.site.register(Profile)

