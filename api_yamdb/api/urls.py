from django.urls import include, path
from rest_framework import routers

from .views import TitleViewSet, UserViewSet, get_token, sign_up


router = routers.DefaultRouter()
router.register('titles', TitleViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', sign_up, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
]
