from django.shortcuts import get_object_or_404

from rest_framework import viewsets

from titles.models import Comment, Review, Title


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = ...
    pagination_class = ...

    def get_queryset(self):
        return Review.objects.filter(title=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs.get('title_id'))
        )


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = ...
    pagination_class = ...

    def get_queryset(self):
        return Comment.objects.filter(review=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs.get('review_id'))
        )
