from django.db import models
from django.conf import settings
from services.models import Product
from django.utils.translation import gettext_lazy as _

# Create your models here.
#Models for cart
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart of {self.user.username}'
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'
    
    
#Checkout order models
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending',_('Pending')
        SHIPPED = 'Shipped',_('Shipped')
        DELIVERED = 'Delivered',_('Delivered')
        CANCELED = 'Canceled',_('Cncelled')
        
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vendor = models.ForeignKey('users.Vendor_Profile', related_name='orders', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey('services.Product', on_delete=models.CASCADE)  # Replace 'Product' with your actual product model
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Ensures a product is added only once per user

    def __str__(self):
        return f"{self.user.username}'s wishlist item: {self.product.name}"