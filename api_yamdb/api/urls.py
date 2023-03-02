from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, signup, token)

v1_router = DefaultRouter()

v1_router.register('users', UserViewSet)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', token, name='token'),
    path('v1/auth/signup/', signup, name='signup')
]
