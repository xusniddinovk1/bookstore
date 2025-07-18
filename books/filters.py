from django_filters import rest_framework as django_filters
from books.models import Book, Author, Category, FlashSale


class BookFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['category', 'max_price', 'min_price']


class AuthorFilter(django_filters.FilterSet):
    class Meta:
        model = Author
        fields = ['name']


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = ['name']


class FlashSaleFilter(django_filters.FilterSet):
    min_discount_percentage = django_filters.NumberFilter(field_name='discount_percentage', lookup_expr='gte')
    max_discount_percentage = django_filters.NumberFilter(field_name='discount_percentage', lookup_expr='lte')
    book = django_filters.CharFilter(field_name='book__title', lookup_expr='icontains')

    class Meta:
        model = FlashSale
        fields = ['min_discount_percentage', 'max_discount_percentage', 'book']
