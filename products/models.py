from account.models import VendorProfile
from django.db import models

class Category(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = "category"
        unique_together = ('vendor', 'name')

class SubCategory(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name="subcategories")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='sub_category_images/', null=True, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = "subcategory"
        unique_together = ('vendor', 'category', 'name')

class Product(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)  # Example: USD, EUR, etc.
    description = models.TextField()
    
    # Category and Sub Category (ForeignKey relationships)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    
    # Image fields for multiple images
    image_1 = models.ImageField(upload_to='product_images/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='product_images/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='product_images/', null=True, blank=True)
    
    quantity = models.CharField(max_length=100)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Timestamps for product creation and update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "products"
        unique_together = ('vendor', 'category','subcategory', 'name')