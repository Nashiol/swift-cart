from django.db.models import Count
from .models import UserProductInteraction, Product, FeaturedProduct

def get_featured_products_for_user(user):
    # Fetch interactions for the user
    interactions = UserProductInteraction.objects.filter(user=user)

    # Get product ids with interaction counts
    product_ids = (
        interactions
        .values('product_id')
        .annotate(interaction_count=Count('id'))
        .order_by('-interaction_count')[:10]
    )

    # If no interactions found, return some fallback featured products
    if not product_ids:
        return FeaturedProduct.objects.filter(is_active=True)  # Or another condition

    # Get products based on the interaction counts
    return Product.objects.filter(id__in=[p['product_id'] for p in product_ids])

