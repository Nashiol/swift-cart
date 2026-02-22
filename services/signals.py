# services/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, FeaturedProduct

@receiver(post_save, sender=Product)
def create_featured_product(sender, instance, created, **kwargs):
    if created:  
        FeaturedProduct.objects.create(product=instance)
