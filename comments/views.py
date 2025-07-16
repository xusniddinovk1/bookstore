from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from comments.serializers import CommentSerializer
from comments.models import Comment
from orders.models import OrderItem


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        book = serializer.validated_data['book']

        # ❗ Faqat sotib olingan kitobga izoh qoldirish mumkin
        if not OrderItem.objects.filter(order__user=user, book=book).exists():
            raise ValidationError("Siz bu kitobni sotib olmagansiz, izoh qoldirolmaysiz.")

        serializer.save(user=user)
