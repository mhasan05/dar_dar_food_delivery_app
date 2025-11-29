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
    pickup_address = serializers.SerializerMethodField()
    drop_address = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user','total_order_items','pickup_address','drop_address', 'order_items', 'total_price', 'status', 'delivery_address','rider','rider_info', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at', 'total_price','rider_info']

    def get_total_order_items(self, obj):
        return obj.order_items.count()
    
    def get_pickup_address(self, obj):
        """
        Pickup address = vendor shop address of the FIRST product in this order.
        (All products must be from the same vendor)
        """
        first_item = obj.order_items.first()
        if first_item and first_item.product.vendor:
            return first_item.product.vendor.current_location
        return None

    def get_drop_address(self, obj):
        """Drop address = order.delivery_address"""
        return obj.user.current_location
