from rest_framework import serializers

from rest_framework.validators import UniqueValidator
from reviews.models import Category, Genre, Title, User


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    slug = serializers.SlugField(required=True)

    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    slug = serializers.SlugField(required=True)

    class Meta:
        model = Category
        exclude = ('id',)


class TitleGetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    year = serializers.IntegerField(required=True)
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = (
            'id',
            'rating',
        )


# Работает через костыли, вариантов по лучше в голову не лезет
class TitleSerializer(TitleGetSerializer):
    genre = serializers.SlugField(required=True)
    category = serializers.SlugField(required=True)

    def create(self, validated_data):
        if Genre.objects.filter(slug=validated_data['genre']).exists():
            genre = Genre.objects.get(slug=validated_data['genre'])
            validated_data.pop('genre')
            if Category.objects.filter(
                slug=validated_data['category']
            ).exists():
                category = Category.objects.get(
                    slug=validated_data['category']
                )
                validated_data.pop('category')
                title = Title(
                    category=category, **validated_data
                )
                title.save()
                title.genre.add(genre)
                return title
        raise serializers.ValidationError


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class SignUpSerializer(serializers.ModelSerializer):
    """
    Поля email и username должны быть уникальными.
    Использовать имя 'me' в качестве username запрещено.
    """
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Имя пользователя <me> недопустимо.'
            )
        return value

    class Meta:
        fields = ('username', 'email')
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
