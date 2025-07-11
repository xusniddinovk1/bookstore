from django.urls import path, include
from books.views import AuthorViewSet, BookViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'author', AuthorViewSet)

urlpatterns = [
    path('', include(router.urls))
]
