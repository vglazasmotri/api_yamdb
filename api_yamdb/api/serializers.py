from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from django.db.models import Avg
from rest_framework import serializers, validators
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title, User
from .validators import validate_username, validate_year


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=256)
    slug = serializers.SlugField(
        required=True,
        max_length=50,
        validators=[validators.UniqueValidator(queryset=Genre.objects.all())],
    )

    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=256)
    slug = serializers.SlugField(
        required=True,
        max_length=50,
        validators=[
            validators.UniqueValidator(queryset=Category.objects.all())
        ],
    )

    class Meta:
        model = Category
        exclude = ('id',)


class TitleGetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=256)
    year = serializers.IntegerField(required=True)
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('id',)

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(rating=Avg('score'))
        if not rating['rating']:
            return None
        return int(rating['rating'])


class TitleSerializer(TitleGetSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        required=False,
        many=True,
        slug_field='slug',
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        required=False,
        slug_field='slug',
    )
    year = serializers.IntegerField(
        required=True,
        validators=(validate_year,),
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['genre'] = GenreSerializer(
            instance=instance.genre, read_only=True, many=True
        ).data
        representation['category'] = CategorySerializer(
            instance=instance.category, read_only=True
        ).data
        return representation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class SignUpSerializer(serializers.Serializer):
    """
    Поля email и username должны быть уникальными.
    Использовать имя 'me' в качестве username запрещено.
    """

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(validate_username, UnicodeUsernameValidator()),
    )
    email = serializers.EmailField(required=True, max_length=254)

    def validate(self, data):
        try:
            User.objects.get_or_create(
                username=data.get('username'), email=data.get('email')
            )
        except IntegrityError:
            raise serializers.ValidationError(
                'Пользователь с таким username или email уже существует.'
            )
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(slug_field='text', read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True,
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Нельзя добавить более одного отзыва')
        return data

    class Meta:
        model = Review
        fields = '__all__'
