from django.urls import include, path
from rest_framework import routers

from .views import TitleViewSet


router = routers.DefaultRouter()
router.register('titles', TitleViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
