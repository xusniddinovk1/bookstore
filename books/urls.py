from django.urls import path, include
from books.views import AuthorViewSet, BookViewSet
from rest_framework.routers import DefaultRouter
from orders.views import OrderViewSet
from comments.views import CommentViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'author', AuthorViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'orders', OdrderViewSet)

urlpatterns = [
    path('', include(router.urls))
]
