from django.db.models import Avg
from rest_framework import serializers
from books.models import Author, Book, Category


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'avg_rating', 'stock', 'created_at']

    def get_avg_rating(self, obj):
        avg = obj.comments.aggregate(avg=Avg('rating'))['avg']
        return round(avg, 2) if avg else None


class BookCreateSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author'
    )

    class Meta:
        model = Book
        fields = ['title', 'author_id', 'price', 'stock']
