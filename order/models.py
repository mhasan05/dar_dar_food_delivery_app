from django.db import models
from account.models import UserAuth  # Assuming this is where UserAuth is defined
from products.models import Product  # Assuming Product model is in product app
from account.models import RiderProfile

# Order Model
class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', 'PENDING'
        CONFIRMED = 'CONFIRMED', 'CONFIRMED'
        ASSIGNED = 'ASSIGNED', 'ASSIGNED'
        DELIVERED = 'DELIVERED', 'DELIVERED'
        CANCELLED = 'CANCELLED', 'CANCELLED'

    user = models.ForeignKey(UserAuth, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    delivery_address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Total price
    rider = models.ForeignKey(RiderProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_orders')
    final_delivery_time = models.DateTimeField(null=True, blank=True)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_rider_assigned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "order"

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"

# OrderItem Model (Intermediate model between Order and Product)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product in the order
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Store product price at the time of order

    class Meta:
        unique_together = ('order', 'product')  # Prevent multiple instances of the same product in one order

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

