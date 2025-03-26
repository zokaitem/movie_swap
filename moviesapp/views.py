from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .models import MovieRecommendation, Tag, Movie
from django.contrib.auth import password_validation
from .forms import RecommendationForm, MovieForm
from django.views.generic.edit import FormMixin
from django.views import generic
import random

def index(request):
    tags = Tag.objects.all()
    trending_movies = MovieRecommendation.objects.order_by('-created_at')[:5]  # trending logic
    return render(request, 'home.html', {'trending_movies': trending_movies,
                                         'tags': tags})


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
        # pasiimame reikšmes iš registracijos formos
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

                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
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

# for testing
# def test_cover(request):
#     movie = Movie.objects.first()
#     if movie.cover:
#         return HttpResponse(f"Cover URL: {movie.cover.url}")
#     return HttpResponse("No cover")

