from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from . import serializers
from titles.models import Comment, Review, Title

RATING_DIGITS_SHOWN = 2


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = ...
    pagination_class = PageNumberPagination
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(title=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        ratings = Review.objects.filter(title=title).values_list('score')
        title.rating = round(
            (sum(ratings) + serializer.data.get('score')) / (len(ratings) + 1),
            RATING_DIGITS_SHOWN
        )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = ...
    pagination_class = PageNumberPagination
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(review=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs.get('review_id'))
        )
