from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title, User


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


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
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
        read_only=True
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
