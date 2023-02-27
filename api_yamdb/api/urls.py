from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/revies/(?P<review_id>)/comments',
    CommentViewSet, basename='comments'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)

urlpatterns = [
    path('', include(router.urls)),
]
