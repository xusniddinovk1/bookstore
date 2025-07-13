from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = ['id', 'user', 'phone_number', 'book', 'amount', 'total_price', 'is_paid', 'created_at']
        read_only_fields = ['user', 'status', 'total_price', 'created_at']

    def get_total_price(self, obj):
        return obj.book.price * obj.amount

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
