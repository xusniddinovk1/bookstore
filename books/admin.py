from django.contrib import admin
from books.models import Book, Author, Category

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book)
