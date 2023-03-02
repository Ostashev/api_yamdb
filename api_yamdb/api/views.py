from rest_framework import viewsets

from titles.models import Genre, Category, Title


class GenreViewSet(viewsets.ModelViewSet):
    """Получить список всех жанров."""
    queryset = Genre.objects.all()
    serializer_class = ()
    permission_classes = ()
    filter_backends = ()
    search_fields = ('name', )


class CategoryViewSet(viewsets.ModelViewSet):
    """Получить список всех категорий. Права доступа: Доступно без токена."""
    queryset = Category.objects.all()
    serializer_class = ()
    permission_classes = ()
    filter_backends = ()
    search_fields = ('name', )


class TitleViewSet(viewsets.ModelViewSet):
    """Получить список всех объектов."""
    queryset = Title.objects.all()
    permission_classes = ()
    filter_backends = ()
