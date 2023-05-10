from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, status, viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Title, User
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleGetSerializer,
    TokenSerializer,
    UserSerializer,
    SignUpSerializer,
)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # authentication_classes = ()
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        print(self.request)
        if self.action == 'list':
            return TitleGetSerializer
        return TitleSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # authentication_classes = ()
    lookup_field = 'slug'
    http_method_names = (
        'get',
        'post',
        'delete',
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination

    def destroy(self, request, *args, **kwargs):
        if self.request.user == permissions.IsAdminUser:
            return super().destroy(request, *args, **kwargs)
        raise PermissionDenied()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # authentication_classes = ()
    lookup_field = 'slug'
    http_method_names = (
        'get',
        'post',
        'delete',
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination

    def destroy(self, request, *args, **kwargs):
        if self.request.user == permissions.IsAdminUser:
            return super().destroy(request, *args, **kwargs)
        raise PermissionDenied()
        
        
class UserViewSet(viewsets.ModelViewSet):
    "Получить список всех пользователей. Права доступа: Администратор."
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["POST"])
def sign_up(request):
    """
    Регистрация нового пользователя.
    Получить код подтверждения на переданный email.
    Права доступа: Доступно без токена.
    """
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Подтверждение регистрации api_yamdb.',
        f'Код подтверждения: {confirmation_code}',
        'from@api_yamdb.com',
        [user.email],
        fail_silently=True,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    """
    Получение JWT-токена в обмен на username и confirmation code.
    Права доступа: Доступно без токена.
    """
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
