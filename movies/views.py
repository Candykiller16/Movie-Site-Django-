from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView

from .models import Movie
from django.views.generic.base import View

from .forms import RewiesForm


class MoviesView(ListView):
    """Список фильмов"""

    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movie_list.html'

    # def get(self, request):
    #     movies = Movie.objects.all()
    #     context = {'movie_list': movies}
    #     return render(request, 'movie_list.html', context)


class MovieDetailView(DetailView):
    """Полное описание фильма"""

    model = Movie
    slug_field = "url"
    template_name = 'movies/movie_detail.html'

    # def get(self, request, slug):
    #     movie = Movie.objects.get(url=slug)
    #     context = {'movie': movie}
    #     return render(request, 'movies/movie_detail.html', context)


class AddReviewView(View):
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
