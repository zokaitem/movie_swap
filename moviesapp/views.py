from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .models import MovieRecommendation, Tag, Movie
from django.contrib.auth import password_validation
from .forms import RecommendationForm, MovieForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views import generic
from django.conf import settings
import requests
import random

def index(request):
    tags = Tag.objects.all()
    url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={settings.TMDB_API_KEY}&language=en-US&page=1"

    response = requests.get(url)
    data = response.json()

    top_rated_movies = data.get('results', []) [:7]
    # trending_movies = MovieRecommendation.objects.order_by('-created_at')[:5]  # trending logic

    return render(request, 'home.html', {'top_rated_movies': top_rated_movies,
                                         'tags': tags})

def top_rated_movies(request):
    url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={settings.TMDB_API_KEY}&language=en-US&page=1"

    page_number = request.GET.get('page', 1)
    top_rated_movies = []
    error_message = None
    total_pages = 1

    try:
        for page in range(1, 26):
            url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={settings.TMDB_API_KEY}&language=en-US&page={page}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            top_rated_movies.extend(data.get('results', []))
            total_pages = data.get('total_pages')
            if page >= total_pages:
                break

        paginator = Paginator(top_rated_movies, 20)
        page_obj = paginator.get_page(page_number)


    except requests.exceptions.RequestException as e:
        error_message = f"An error occurred while fetching top-rated movies: {e}"

    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"

    return render(request, 'top_rated.html', {'page_obj': page_obj if not error_message else [],
                                              'error_message': error_message,
                                              'total_pages': total_pages,
                                              'top_rated_movies': top_rated_movies,
                                         })


def get_recommendation_guest(request):

    tag = request.GET.get('tag','').strip()

    print("Tag from request:", repr(tag))
    print("Available tags in DB:", list(MovieRecommendation.objects.values_list('tag__name', flat=True)))
    request.session['selected_tag'] = tag
    request.session['skip_count'] = 0

    if tag:
        recommendation = MovieRecommendation.objects.filter(tag__name__iexact=tag).order_by('?').first()
        if not recommendation:
            recommendation = MovieRecommendation.objects.order_by('?').first()
    else:
        recommendation = MovieRecommendation.objects.order_by('?').first()

    if recommendation:
        return render(request, 'recommendation_guest.html', {'recommendation': recommendation, 'selected_tag': tag, 'cover_url': recommendation.movie.cover.url if recommendation.movie.cover else None})
    else:
        return render(request, 'recommendation_guest.html', {
            'error': "No recommendations available at the moment."
        })

def skip_recommendation(request, recommendation_id):
    tag = request.session.get('selected_tag')
    skip_count = request.session.get('skip_count', 0)


    if not request.user.is_authenticated and request.session['skip_count'] >= 1:
        messages.error(request, 'Please log in or register for unlimited skips')
        return redirect('get_recommendation_guest')
    request.session['skip_count'] = skip_count + 1
    request.session.modified = True

    new_recommendation = MovieRecommendation.objects.filter(tag__name__iexact=tag).exclude(id=recommendation_id).order_by('?').first()
    if new_recommendation:
        return render(request, 'recommendation_guest.html', {'recommendation': new_recommendation, 'selected_tag': tag, 'cover_url': new_recommendation.movie.cover.url if new_recommendation.movie.cover else None})
    else:
        # messages.error(request, 'No more recommendations for this tag')
        # return redirect('get_recommendation_guest')
        return render(request, 'recommendation_guest.html', {'error': "No more recommendations for this tag", 'recommendation': None,
        'selected_tag': tag})

def success_page(request):
    return render(request, 'success.html')

@login_required
def submit_recommendation(request):
    form = RecommendationForm()


    if request.method == 'POST':
        form = RecommendationForm(request.POST)


        if form.is_valid():

            recommendation = form.save(commit=False)
            recommendation.user = request.user
            recommendation.save()
            return redirect('success')
        else:
            form = RecommendationForm()

    return render(request, 'submit_recommendation.html', {'form': form})

def add_movie(request):
    movie_form = MovieForm()

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('submit_recommendation')
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form})


@csrf_protect
def register(request):
    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'User name {username} already exists')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'User with such email {email} already exists!')
                    return redirect('register')
                else:
                    try:
                        password_validation.validate_password(password)
                    except password_validation.ValidationError as e:
                        for error in e:
                            messages.error(request, error)
                        return redirect('register')


                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'User {username} registered!')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    return render(request, 'register.html')

class MovieListView(generic.ListView):
    model = Movie
    template_name = "movies.html"
    context_object_name = "movies"

class MovieDetailView(generic.DetailView):
    model = Movie
    template_name = "movie.html"
    context_object_name = "movie"


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        new_email = request.POST['email']
        if new_email == "":
            messages.error(request, f"Email field can't be empty")
            return redirect('profile')
        if request.user.email != new_email and User.objects.filter(email=new_email).exists():
            messages.error(request, f'User with such email already exists')
            return redirect('profile')
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile updated")
            return redirect('profile')


    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, "profile.html", context=context)


def get_popular_movies(request):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={settings.TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url)
    data = response.json()

    context = {
        'movies': data.get('results', [])
    }
    return render(request, 'popular.html', context)


# for testing
# def test_cover(request):
#     movie = Movie.objects.first()
#     if movie.cover:
#         return HttpResponse(f"Cover URL: {movie.cover.url}")
#     return HttpResponse("No cover")

