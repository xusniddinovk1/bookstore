from orders.permissions import IsOwnerOrReadOnly
from .serializers import OrderSerializer
from .models import Order
from rest_framework import viewsets


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)