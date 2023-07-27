from rest_framework import serializers
from django.shortcuts import get_object_or_404


from .models import Movie, RatingsChoices, MovieOrder
from users.models import User


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, required=False)
    rating = serializers.ChoiceField(
        choices=RatingsChoices.choices, required=False, default=RatingsChoices.G
    )
    synopsis = serializers.CharField(required=False)
    added_by = serializers.ReadOnlyField(source="user.email")

    def create(self, validated_data):
        user_name = self.context["request"].user
        user = User.objects.get(username=user_name)

        movie = Movie.objects.create(user=user, **validated_data)
        return movie


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    title = serializers.CharField(source="movie.title", read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_by = serializers.EmailField(source="user.email", read_only=True)
    buyed_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        movie_order = MovieOrder.objects.create(**validated_data)

        return movie_order
