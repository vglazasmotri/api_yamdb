from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, status, viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import  action, api_view, permission_classes
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User
from .permissions import (IsAdminModeratorOwnerOrReadOnly, IsAdmin)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleGetSerializer,
    TokenSerializer,
    UserSerializer,
    ReviewSerializer,
    SignUpSerializer,
    CommentSerializer,
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
    lookup_field = 'username'
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    @action(
        methods=['GET', 'PATCH'], detail=False, url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_update_me(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            if self.request.method == 'PATCH':
                serializer.validated_data.pop('role', None)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def sign_up(request): 
    """
    Регистрация нового пользователя.
    Получить код подтверждения на переданный email.
    Права доступа: Доступно без токена.
    """
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
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
@permission_classes([permissions.AllowAny])
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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))

        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
