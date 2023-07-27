from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .permissions import PermissionForMovieAuthView
from .models import Movie
from .serialzers import MovieSerializer, MovieOrderSerializer


class MovieAuthView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [PermissionForMovieAuthView]

    def post(self, request: Request):
        serializer = MovieSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request: Request):
        movies = Movie.objects.all()

        result_page = self.paginate_queryset(movies, request, view=self)

        serializer = MovieSerializer(data=result_page, many=True)
        serializer.is_valid()

        return self.get_paginated_response(serializer.data)


class MovieAuthDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [PermissionForMovieAuthView]

    def get(self, request: Request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieSerializer(movie)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)

        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MoviesOrderAuthDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user, movie=movie)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
