from django.db import models
from django.conf import settings
from account.models import VendorProfile



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    icon = models.ImageField(upload_to='categories/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "Categories"
        db_table = "category"
    
    def __str__(self):
        return self.name


class Product(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    stock_qty = models.PositiveIntegerField(default=0)
    is_out_of_stock = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_glosary = models.BooleanField(default=False)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    dimensions = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Products"
        db_table = "product"
    
    def __str__(self):
        return self.name
