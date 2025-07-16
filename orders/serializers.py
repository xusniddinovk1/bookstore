from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import Order, OrderItem
from books.models import Book


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = ['id', 'user', 'phone_number', 'book', 'amount', 'total_price', 'is_paid', 'created_at']
        read_only_fields = ['user', 'status', 'total_price', 'created_at']

    def get_total_price(self, obj):
        return obj.book.price * obj.amount

    def validate_quantity(self, value):
        try:
            book_id = self.initial_data['book']
            book = Book.objects.get(id=book_id)

            if value > book.stock:
                raise serializers.ValidationError('Not enough items in stock')
            if value < 1:
                raise serializers.ValidationError('Value must be at least 1')
            return value
        except ObjectDoesNotExist:
            return serializers.ValidationError('Book does not exist')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        order = Order.objects.create(**validated_data)
        book = order.book
        book.stock -= order.amount
        book.save()
        return order


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['book', 'quantity']
