from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import OrderProductSerializer  # Assuming you have a ProductSerializer
from account.serializers import RiderProfileSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderProductSerializer(read_only=True)  # Nested product data

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)  # No need for source
    total_order_items = serializers.SerializerMethodField()
    rider_info = RiderProfileSerializer(source='rider', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user','total_order_items', 'order_items', 'total_price', 'status', 'delivery_address','rider','rider_info', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at', 'total_price','rider_info']

    def get_total_order_items(self, obj):
        return obj.order_items.count()
