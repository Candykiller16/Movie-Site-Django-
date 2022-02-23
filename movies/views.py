from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView

from .models import Movie, Category, Actor, Genre
from django.views.generic.base import View

from .forms import RewiesForm


class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class MoviesView(GenreYear, ListView):
    """Список фильмов"""

    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movie_list.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context

    # def get(self, request):
    #     movies = Movie.objects.all()
    #     context = {'movie_list': movies}
    #     return render(request, 'movie_list.html', context)


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""

    model = Movie
    slug_field = "url"
    template_name = 'movies/movie_detail.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context

    # def get(self, request, slug):
    #     movie = Movie.objects.get(url=slug)
    #     context = {'movie': movie}
    #     return render(request, 'movies/movie_detail.html', context)


class AddReviewView(GenreYear, View):
    """Отзывы"""

    def post(self, request, pk):
        form = RewiesForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """Вывод информации об актере"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name"


class FilterMovieView(GenreYear, ListView):
    """Фильтр фильмов"""

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genres"))
        )
        # фильтрация,которая будет обрабатываться после получения с frontend
        return queryset
