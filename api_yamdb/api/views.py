from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Title, User
from .serializers import TitleSerializer, TokenSerializer, UserSerializer, SignUpSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # authentication_classes = ()


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
    Использовать имя 'me' в качестве username запрещено.
    Поля email и username должны быть уникальными.
    """
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    # Отпрака письма с кодом подтверждения.
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
    # Получение из модели и проверка кода подтверждения
    confirmation_code = True
    if confirmation_code == True:
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
