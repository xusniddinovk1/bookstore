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
    discounted_price = serializers.SerializerMethodField()
    flash_sale_active = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category', 'price', 'discounted_price',
                  'flash_sale_active', 'avg_rating', 'stock', 'created_at']

    def get_avg_rating(self, obj):
        avg = obj.comments.aggregate(avg=Avg('rating'))['avg']
        return round(avg, 2) if avg else None

    def get_discounted_price(self, obj):
        return obj.get_discounted_price()

    def get_flash_sale_active(self, obj):
        return bool(obj.get_active_flash_sale())


class BookCreateSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author'
    )

    class Meta:
        model = Book
        fields = ['title', 'author_id', 'category', 'price', 'stock']
