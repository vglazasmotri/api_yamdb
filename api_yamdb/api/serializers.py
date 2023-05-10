from rest_framework import serializers

from reviews.models import Category, Genre, Title


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
