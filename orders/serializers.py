from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['book', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)  # nested
    total_price = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = ['id', 'user', 'phone_number', 'items', 'total_price', 'is_paid', 'created_at']
        read_only_fields = ['user', 'total_price', 'created_at']

    def get_total_price(self, obj):
        return sum([item.book.price * item.quantity for item in obj.items.all()])

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(user=user, **validated_data)

        for item_data in items_data:
            book = item_data['book']
            quantity = item_data['quantity']

            if quantity > book.stock:
                raise serializers.ValidationError(
                    f"Book '{book.title}' only has {book.stock} in stock."
                )

            OrderItem.objects.create(order=order, book=book, quantity=quantity)

            # Reduce stock
            book.stock -= quantity
            book.save()

        return order
