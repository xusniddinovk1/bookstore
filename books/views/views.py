from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from django_filters import rest_framework as django_filters
from rest_framework import filters
from books.filters import BookFilter
from books.serializers import BookSerializer, BookCreateSerializer
from books.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from books.models import Book
from books.pagination import Pagination
from django.db import models


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    pagination_class = Pagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = BookFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BookCreateSerializer
        return BookSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('min_price', openapi.IN_QUERY, description="Narxdan katta yoki teng",
                          type=openapi.TYPE_NUMBER),
        openapi.Parameter('max_price', openapi.IN_QUERY, description="Narxdan kichik yoki teng",
                          type=openapi.TYPE_NUMBER),
        openapi.Parameter('category', openapi.IN_QUERY, description="Kategoriya nomi (qisman)",
                          type=openapi.TYPE_STRING),
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_books = Book.objects.filter(author=instance.author).exclude(id=instance.id)[:3]
        related_serializer = BookSerializer(related_books, many=True)
        return Response({
            'book': serializer.data,
            'related_books': related_serializer.data
        })

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        top_books = Book.objects.annotate(avg_rating=models.Avg('comments__rating')).order_by('-avg_rating')[:2]
        serializers = BookSerializer(top_books, many=True)
        return Response(serializers.data)

    @action(detail=True, methods=['get'])
    def avg_rating(self, request, pk=None):
        book = self.get_object()
        comments = book.comments.all()  # To'g'ri manager

        if comments.count() == 0:
            return Response({'average_rating': 'No comments yet'})

        avg_rating = sum([comment.rating for comment in comments]) / comments.count()
        return Response({'average_rating': round(avg_rating, 2)})
