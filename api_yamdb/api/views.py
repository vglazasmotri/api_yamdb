from rest_framework import filters, viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import PermissionDenied

from reviews.models import Category, Genre, Title
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleGetSerializer,
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
