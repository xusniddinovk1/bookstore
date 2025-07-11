from rest_framework.response import Response
from rest_framework import viewsets
from books.serializers import AuthorSerializer, BookSerializer, BookCreateSerializer
from books.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from books.models import Author, Book
from books.pagination import Pagination


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = Pagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        books = Book.objects.filter(author=instance).values_list('title', flat=True)[:3]
        return Response({
            'author': serializer.data,
            'books': list(books)
        })


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    pagination_class = Pagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BookCreateSerializer
        return BookSerializer
