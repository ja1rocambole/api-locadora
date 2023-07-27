from django.urls import path
from .views import MovieAuthView, MovieAuthDetailView, MoviesOrderAuthDetailView

urlpatterns = [
    path("movies/", MovieAuthView.as_view()),
    path("movies/<int:movie_id>/", MovieAuthDetailView.as_view()),
    path("movies/<int:movie_id>/orders/", MoviesOrderAuthDetailView.as_view()),
]
