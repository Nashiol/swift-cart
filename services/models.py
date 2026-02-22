from django.db import models
from users.models import Vendor_Profile
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

#Models for products
class ProductImage(models.Model):
    product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f'image for {self.product.name}'

class Product(models.Model):

    STATUS_CHOICES = (
        ('used_good', 'used - Good Condition'), 
        ('used_excellent', 'used - Excellent Condition'), 
        ('Brand_new', ' Brand New'), 
    )

    vendor = models.ForeignKey(Vendor_Profile, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveBigIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='brand_new', 
    )

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=225, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name'] #Order by name field in ascending order
        db_table = 'Categories'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class NewsLetterSubscription(models.Model):
    email = models.EmailField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    
class FeaturedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='featured')
    date_featured = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Optional
    FEATURE_TYPES = [
        ('RECOMMENDED', 'Recommended'),
        ('TRENDING', 'Trending'),
        ('TOP_SELLER', 'Top Seller'),
    ]
    feature_type = models.CharField(max_length=20, choices=FEATURE_TYPES, default='RECOMMENDED')  # Optional

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product'], name='unique_featured_product'),
        ]
        indexes = [
            models.Index(fields=['date_featured']),
        ]

    def __str__(self):
        return f'Featured: {self.product.name} ({self.feature_type})'


class Review(models.Model):
    vendor = models.ForeignKey(Vendor_Profile, on_delete=models.CASCADE, related_name="reviews")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=1)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer.username} for {self.vendor.business_name}"

    class Meta:
        ordering = ['-created_at']  # Sort reviews by the most recent


class UserProductInteraction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=20, choices=[
        ('view', 'View'),
        ('wishlist', 'Wishlist'),
        ('cart', 'Cart'),
        ('like', 'Like'),
    ])
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Optional, if you need to mark interactions as inactive
    
    class Meta:
        unique_together = ('user', 'product', 'interaction_type')  # Prevent duplicate interactions
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['product']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f'{self.user} - {self.product} - {self.interaction_type}'
