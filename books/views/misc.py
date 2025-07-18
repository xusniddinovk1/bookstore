from rest_framework.response import Response
from rest_framework import viewsets, filters
from books.filters import AuthorFilter, CategoryFilter, FlashSaleFilter
from books.serializers import AuthorSerializer, BookSerializer, CategorySerializer, \
    FlashSaleSerializer
from books.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from books.models import Author, Book, Category, FlashSale
from books.pagination import Pagination
from orders.permissions import IsOwnerOrReadOnly
from django_filters import rest_framework as django_filters


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filterset_class = CategoryFilter


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = Pagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filterset_class = AuthorFilter
    search_fields = ['name']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        books = Book.objects.filter(author=instance).values_list('title', flat=True)[:3]
        related_books = Book.objects.filter(book=instance).exclude(id=instance.id)[:3]
        related_serializer = BookSerializer(related_books, many=True)
        return Response({
            'author': serializer.data,
            'books': list(books),
            'related_books': related_serializer.data
        })


class FlashSaleViewSet(viewsets.ModelViewSet):
    queryset = FlashSale.objects.all()
    serializer_class = FlashSaleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = FlashSaleFilter
