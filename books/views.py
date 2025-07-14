from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from books.serializers import AuthorSerializer, BookSerializer, BookCreateSerializer, CategorySerializer
from books.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from books.models import Author, Book, Category
from books.pagination import Pagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = Pagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

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


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    pagination_class = Pagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BookCreateSerializer
        return BookSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_books = Book.objects.filter(author=instance.author).exclude(id=instance.id)[:3]
        related_serializer = BookSerializer(related_books, many=True)
        return Response({
            'book': serializer.data,
            'related_books': related_serializer.data
        })

    @action(detail=True, methods=['get'])
    def avg_rating(self, request, pk=None):
        book = self.get_object()
        comments = book.comments.all()  # To'g'ri manager

        if comments.count() == 0:
            return Response({'average_rating': 'No comments yet'})

        avg_rating = sum([comment.rating for comment in comments]) / comments.count()
        return Response({'average_rating': round(avg_rating, 2)})
