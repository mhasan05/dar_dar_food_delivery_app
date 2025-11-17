from rest_framework import serializers
from .models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    def validate_price(self, value):
        # Ensure price is not negative
        if value < 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value
    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Rating must be between 0 and 5.")
        return value
