import re

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from .models import Movie
from .models import MovieList


# Create your views here.
@login_required(login_url="account_login")
def index(request):
    movies = Movie.objects.all()
    featured_movie = movies[len(movies) - 1]

    context = {
        "movies": movies,
        "featured_movie": featured_movie,
    }
    return render(request, "core/index.html", context)


@login_required(login_url="account_login")
def movie(request, pk):
    movie_uuid = pk
    movie_details = Movie.objects.get(uu_id=movie_uuid)

    context = {
        "movie_details": movie_details,
    }

    return render(request, "core/movie.html", context)


@login_required(login_url="account_login")
def genre(request, pk):
    movie_genre = pk
    movies = Movie.objects.filter(genre=movie_genre)

    context = {
        "movies": movies,
        "movie_genre": movie_genre,
    }
    return redirect(request, "core/genre.html", context)


@login_required(login_url="account_login")
def search(request):
    if request.method == "POST":
        search_term = request.POST["search_term"]
        movies = Movie.objects.filter(title__icontains=search_term)

        context = {
            "movie": movies,
            "serach_term": search_term,
        }
        return render(request, "core/search.html", context)
    return redirect("core/")


@login_required(login_url="account_login")
def my_list(request):
    movie_list = MovieList.objects.filter(owner_user=request.user)
    user_movie_list = []

    for movie in movie_list:
        user_movie_list.append(movie.movie)

    context = {
        "movies": user_movie_list,
    }
    return render(request, "core/my_list.html", context)


@login_required(login_url="account_login")
def add_to_list(request):
    if request.method == "POST":
        movie_url_id = request.POST.get("movie_id")
        uuid_pattern = r"[0-9a-f]{8}-[0-9a-f]{4}[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
        match = re.search(uuid_pattern, movie_url_id)
        movie_id = match.group() if match else None

        movie = get_object_or_404(Movie, uu_id=movie_id)
        movie_list, created = MovieList.objects.get_or_create(
            owner_user=request.user,
            movie=movie,
        )

        if created:
            response_data = {"status": "success", "message": "Added"}

        else:
            response_data = {"status": "Info", "message": "movie already in list"}

        return JsonResponse(response_data)
    return JsonResponse({"status": " error", "message": " invalid request"}, status=400)
