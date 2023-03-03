from smtplib import SMTPResponseException

from django.shortcuts import render
from django.conf import settings
from rest_framework import status, viewsets
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

from users.models import User
from users.utils import generate_confirmation_code
from .serializers import (UserSerializer, UserAdminSerializer, SignUpSerializer, GetTokenSerializer,
                          CategotySerializer, GenreSerializer, TitleSerializer)
from . permissions import IsAdmin, IsAdminSuperuser, IsAuthorModeratorAdminSuperuserOrReadOnly
from . import serializers
from titles.models import (Comment, Review, Title, 
                           Genre, Category, Title)


RATING_DIGITS_SHOWN = 2


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = (IsAdminSuperuser,)
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('username',)
    search_fields = ('username',)

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated,],
            serializer_class=UserSerializer,
            pagination_class=None,
            queryset=User.objects.all())
    def me(self, request):
        if request.method == 'GET':
            serializer = self.serializer_class(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup(request):
    user = User.objects.filter(**request.data)
    if user.exists():
        get_and_send_confirmation_code(user)
        return Response(request.data, status=status.HTTP_200_OK)

    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        user = User.objects.filter(**serializer.data)
        get_and_send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.data['username'])
    if serializer.data['confirmation_code'] == user.confirmation_code:
        refresh = RefreshToken.for_user(user)
        return Response(
            {'token': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )
    return Response(
        'Проверьте правильность указанных для получения токена данных.',
        status=status.HTTP_400_BAD_REQUEST
    )

def get_and_send_confirmation_code(data):
    confirmation_code = generate_confirmation_code()
    data.update(confirmation_code=confirmation_code)
    subject = 'Ваш код, для получения token.'
    message = f'Для получения token отправьте код {confirmation_code} и имя пользователя на адрес: http://127.0.0.1:8000/api/v1/auth/token/'
    send_mail(subject, message, '123@rt.ru', [data[0].email])


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorModeratorAdminSuperuserOrReadOnly, IsAuthenticatedOrReadOnly)
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
    permission_classes = (IsAuthorModeratorAdminSuperuserOrReadOnly,)
    pagination_class = PageNumberPagination
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(review=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs.get('review_id'))
        )
        
        
class GenreViewSet(viewsets.ModelViewSet):
    """Получить список всех жанров."""
    queryset = Genre.objects.all()
    serializer_class = (GenreSerializer)
    permission_classes = ()
    filter_backends = ()
    search_fields = ('name', )


class CategoryViewSet(viewsets.ModelViewSet):
    """Получить список всех категорий. Права доступа: Доступно без токена."""
    queryset = Category.objects.all()
    serializer_class = (CategotySerializer)
    permission_classes = ()
    filter_backends = ()
    search_fields = ('name', )


class TitleViewSet(viewsets.ModelViewSet):
    """Получить список всех объектов."""
    queryset = Title.objects.all()
    serializer_class = (TitleSerializer)
    permission_classes = (IsAdminSuperuser)
    filter_backends = ()
