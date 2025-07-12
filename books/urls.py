from django.urls import path, include
from books.views import AuthorViewSet, BookViewSet
from rest_framework.routers import DefaultRouter

from comments.views import CommentViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'author', AuthorViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls))
]
