from rest_framework import serializers
from .models import Wishlist
from products.serializers import ProductSerializer

class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
