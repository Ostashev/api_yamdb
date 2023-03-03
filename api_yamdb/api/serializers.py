from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import User
from titles.models import Comment, Review, Category, Genre, Title


class UserSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для эндпоинта 'users/me/' для любого авторизов. пользователя.
    [GET] персональные данные пользователя.
    [POST] заполнение полей 'first_name', 'last_name' и 'bio'.
    """
    role = serializers.StringRelatedField(read_only=True)
    #username = serializers.SlugField(read_only=True)
    #email = serializers.SlugField(max_length=254, read_only=True)

    class Meta:
        model = User
        ordering = ['id']
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserAdminSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для эндпоинта 'users/' для пользователя с ролью 'admin'.
    [GET] получение списка пользователей.
    [POST] регистрация нового пользователя.
    [GET, PATCH, DELETE] работа с пользователем по username.
    """
    class Meta:
        model = User
        ordering = ['id']
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]

    def validate(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено!'
            )
        return value


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, value):
        if value['username'] == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено!'
            )
        return value


class GetTokenSerializer(serializers.Serializer):
    username = serializers.SlugField(required=True)
    confirmation_code = serializers.SlugField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategotySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id', )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id', )


class TitleSerializer(serializers.ModelSerializer):
    category = CategotySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'category',
            'genre',
        )



class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre',
        )



class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    def validate(self, attrs):
        if not (1 <= attrs.get('score') <= 10):
            raise serializers.ValidationError(
                'Score must be an integer value between 1 and 10.')
        return attrs

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author', 'pub_date')
