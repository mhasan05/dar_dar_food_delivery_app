from django.db import models
from account.models import UserAuth
from products.models import Product  # Assuming Product model is in product app

class Wishlist(models.Model):
    user = models.ForeignKey(UserAuth, on_delete=models.CASCADE)  # User owning the wishlist item
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Product added to the wishlist
    created_at = models.DateTimeField(auto_now_add=True)  # When the item was added
    updated_at = models.DateTimeField(auto_now=True)  # When the item was last updated

    class Meta:
        verbose_name_plural = "Wishlists"
        db_table = "wishlist"
        unique_together = ('user', 'product')  # Prevent multiple instances of same product for the same user

    def __str__(self):
        return f"Wishlist - {self.user.email} - {self.product.name}"
