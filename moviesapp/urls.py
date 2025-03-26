"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from.views import (get_recommendation_guest,
                   skip_recommendation,
                   submit_recommendation,
                   success_page,
                   add_movie,
                   register,
                   MovieListView,
                   MovieDetailView,
                   )

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('recommendation/', get_recommendation_guest, name='get_recommendation_guest'),
    path('skip-recommendation/<int:recommendation_id>/', skip_recommendation, name='skip_recommendation'),
    path('submit-recommendation/', submit_recommendation, name='submit_recommendation'),
    path('success/', success_page, name='success'),
    path('add-movie/', add_movie, name='add_movie'),
    path('register/', register, name='register'),
    path('movies/',MovieListView.as_view(), name='movies'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie')
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]