from rest_framework import serializers
from .models import *
from account.serializers import *

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    # vendor_info = VendorProfileSerializer(source='vendor', read_only=True)
    class Meta:
        model = Category
        fields = '__all__'

# SubCategory Serializer
class SubCategorySerializer(serializers.ModelSerializer):
    # vendor_info = VendorProfileSerializer(source='vendor', read_only=True)
    # category = CategorySerializer(read_only=True)  # Nested category data
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = ['id','name','image','vendor','category','category_name']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

class ShopInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = ['id','shop_name','shop_image','shop_license','shop_type','shop_address','phone_number','rating','total_rating_count']


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True)  # Nested category data
    # subcategory = SubCategorySerializer(read_only=True)  # Nested subcategory data
    # vendor_info = serializers.StringRelatedField(source='vendor', read_only=True)  # Vendor info
    shop_info = ShopInfoSerializer(source='vendor', read_only=True)
    vendor_subcategories = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()
    shop_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id','name','description','shop_name','shop_image','category','subcategory','image_1','image_2','image_3','currency','price','quantity','delivery_fee','created_at','updated_at','vendor','shop_info','vendor_subcategories']

    def get_shop_name(self, obj):
        return obj.vendor.shop_name if obj.vendor else None

    def get_shop_image(self, obj):
        # Fetch the shop image from the related VendorProfile
        return obj.vendor.shop_image.url if obj.vendor and obj.vendor.shop_image else None
    

    def get_vendor_subcategories(self, obj):
    # Return all subcategories of THIS product vendor
        subcategories = SubCategory.objects.filter(vendor=obj.vendor)
        return SubCategorySerializer(subcategories, many=True).data





class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','description','image_1','image_2','image_3','price','created_at','updated_at','vendor']





class ShopSubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ['id','name','vendor']
