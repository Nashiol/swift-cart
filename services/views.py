from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, ProductImage, FeaturedProduct, Review, Category, UserProductInteraction
from.forms import ProductForm, NewsletterForm, ReviewForm
from users.models import Vendor_Profile
from django.forms import modelformset_factory
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from random import sample
from services.utils import get_featured_products_for_user
from django.db import connection
import random

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        # Fetch products the user has interacted with, sorted by frequency of interaction
        user_interactions = UserProductInteraction.objects.filter(user=request.user)
        
        # Get products associated with the interactions
        product_interactions = Product.objects.filter(
            userproductinteraction__in=user_interactions
        ).distinct()

        # Get all featured products, including those the user interacted with
        featured_products = FeaturedProduct.objects.filter(
            feature_type='RECOMMENDED', product__isnull=False
        )

        # Shuffle the products for randomness
        featured_products = list(featured_products)  # Convert queryset to list to shuffle
        random.shuffle(featured_products)

        # Limit to 4 featured products
        featured_products = featured_products[:4]

    else:
        # Fetch all featured products (or filter as needed)
        featured_products = FeaturedProduct.objects.filter(
            feature_type='RECOMMENDED', product__isnull=False
        )

        # Limit to 4 featured products
        featured_products = featured_products[:4]
    
    context = {
        'featured_products': featured_products,
    }
    
    return render(request, 'services/home.html', context)





@login_required
def vendor_products(request):
    try:
        # Get the vendor profile for the currently logged-in user
        vendor_profile = Vendor_Profile.objects.get(user=request.user)
    except Vendor_Profile.DoesNotExist:
        return redirect('vendor-signup')  # Redirect to the vendor signup page if vendor profile doesn't exist
    
    # Get all the products associated with the vendor
    products = Product.objects.filter(vendor=vendor_profile)

    if not products:
        # If no products found, display a message to the vendor
        messages.info(request, "You have not added any products yet. Add products to display here.")

    return render(request, 'services/vendor-products.html', {
        'vendor': vendor_profile,
        'products': products,
    })



def add_product(request):
    ImageFormSet = modelformset_factory(ProductImage, fields=('image',), extra=5)

    try:
        vendor_profile = Vendor_Profile.objects.get(user=request.user)
    except Vendor_Profile.DoesNotExist:
        return redirect('vendor-signup')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())

        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.vendor = vendor_profile
            product.status = request.POST.get('status', 'Inactive')  # Set default status if not provided
            product.save()

            for image_form in formset.cleaned_data:
                if image_form:
                    image = image_form['image']
                    ProductImage.objects.create(product=product, image=image)

            return redirect('services:vendor-products')
    else:
        form = ProductForm()
        formset = ImageFormSet(queryset=ProductImage.objects.none())

    return render(request, 'services/add-product.html', {
        'form': form,
        'formset': formset,
    })


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Create a formset for ProductImage
    ProductImageFormSet = modelformset_factory(
        ProductImage, 
        fields=('image',), 
        extra=1,  # Allows adding one new image
        can_delete=True  # Allows removing images
    )

    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, queryset=product.images.all())

        if product_form.is_valid() and formset.is_valid():
            product = product_form.save(commit=False)
            product.status = request.POST.get('status', product.status)  # Update status or keep the current one
            product.save()

            # Save images through the formset
            instances = formset.save(commit=False)
            for instance in instances:
                instance.product = product
                instance.save()
            
            # Handle deletions
            for deleted in formset.deleted_objects:
                deleted.delete()

            return redirect('services:vendor-products')
    else:
        product_form = ProductForm(instance=product)
        formset = ProductImageFormSet(queryset=product.images.all())

    return render(request, 'services/edit-product.html', {
        'product_form': product_form,
        'formset': formset,
    })



@login_required
def delete_product(request, pk):
    # Ensure the product exists and belongs to the logged-in vendor's profile
    vendor_profile = get_object_or_404(Vendor_Profile, user=request.user)
    product = get_object_or_404(Product, pk=pk, vendor=vendor_profile)

    # Delete the product
    product.delete()

    # Add a success message
    messages.success(request, "Product deleted successfully!")

    # Redirect to the vendor's product listing page
    return redirect("services:vendor-products")





from django.core.paginator import Paginator

#Product listings
def product_list(request):
    # Get all categories
    categories = Category.objects.all()

    # Get the category from the request (if any)
    category_name = request.GET.get('category')
    if category_name:
        # Filter products by the selected category
        products = Product.objects.filter(category__name=category_name).select_related('vendor')
    else:
        # Show all products, randomized
        products = Product.objects.select_related('vendor').order_by('?')

    # Pagination logic
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'services/product-list.html', {
        'products': page_obj,
        'categories': categories,
        'selected_category': category_name,
    })

#product details
def product_detail(request, pk):
    # Fetch the Product instance with the given primary key
    product = get_object_or_404(Product, pk=pk)

    # Log the product interaction (if the user is authenticated)
    if request.user.is_authenticated:
        UserProductInteraction.objects.get_or_create(
            user=request.user,
            product=product,
        )

    # Pass the product to the template context
    return render(request, 'services/product-detail.html', {'product': product})









def service(request):
    return render(request, 'services/service.html')

def about_view(request):
    return render(request, 'services/about.html')

def contact_page(request):
    return render(request, 'services/contact.html')


def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            #Send confirmation email.
            send_mail(
                'Newsletter Subscription Confirmation',
                'Thank you for subscribing to out newsletter',
                settings.EMAIL_HOST_USER,
                [form.cleaned_data['email']],
                fail_silently=False,
            )

            return redirect('services:newsletter-thanks')
    else:
        form = NewsletterForm()

    return render(request, 'services/newsletter-signup.html', {'form': form})


def newsletter_thanks(request):
    return render(request, 'services/newsletter-thanks.html')

from .forms import SearchForm
from django.db.models import Q

def search(request):
    form = SearchForm(request.GET)
    products = []
    query = ""  # Initialize query variable

    if form.is_valid():
        query = form.cleaned_data['query'].strip()  # Now correctly accessing 'query' field
        if query:
            # Filter products by name or category name
            products = Product.objects.filter(
                Q(name__icontains=query) | Q(category__name__icontains=query)
            )
    
    # Pass 'query' to the template context
    return render(request, 'services/search-results.html', {'form': form, 'products': products, 'query': query})


from django.http import HttpResponse
from django.template.loader import render_to_string

def export_search_results(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query)  # Example query
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="search_results.txt"'

    for product in products:
        text = render_to_string('search/indexes/services/product_text.txt', {'object': product})
        response.write(text + "\n\n")  # Add spacing between product details

    return response


def vendor_products_list(request, vendor_id):
    vendor_profile = get_object_or_404(Vendor_Profile, id=vendor_id)
    products = Product.objects.filter(vendor=vendor_profile)
    return render(request, 'services/vendor-products-list.html', {'vendor': vendor_profile, 'products': products})



def public_business_profile(request, vendor_id):
    vendor_profile = get_object_or_404(Vendor_Profile, id=vendor_id)
    
    # Get the products uploaded by the vendor
    products = Product.objects.filter(vendor=vendor_profile)
    
    # Get reviews for the vendor's business
    reviews = Review.objects.filter(vendor=vendor_profile).order_by('-created_at')

    # Calculate average rating
    if reviews.exists():
        average_rating = sum(review.rating for review in reviews) / reviews.count()
    else:
        average_rating = 0  # If no reviews, set to 0

    # Process reviews to include filled and empty stars
    for review in reviews:
        review.filled_stars = range(1, review.rating + 1)  # Filled stars
        review.empty_stars = range(review.rating + 1, 6)   # Empty stars

    # Handle the review form submission
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user  # Associate the review with the logged-in user
            review.vendor = vendor_profile  # Associate the review with the vendor's business
            review.save()
            return redirect('services:public-business-profile', vendor_id=vendor_id)
    else:
        form = ReviewForm()

    # Pass a list of numbers (1-5) for the stars
    star_range = [1, 2, 3, 4, 5]

    return render(request, 'services/public-business-profile.html', {
        'profile': vendor_profile,
        'products': products,
        'reviews': reviews,
        'review_form': form,
        'average_rating': average_rating,  # Pass average rating to the template
        'star_range': star_range  # Pass star range for the template
    })



def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    # Ensure the logged-in user is the one who created the review
    if review.customer != request.user:
        return redirect('services:public-business-profile', vendor_id=review.vendor.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('services:public-business-profile', vendor_id=review.vendor.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'services/edit-review.html', {'form': form, 'review': review})



def delete_review(request, review_id):
    # Get the review to be deleted
    review = get_object_or_404(Review, id=review_id)
    
    # Check if the current user is the one who created the review
    if review.customer == request.user:
        # Calculate filled and empty stars based on the review's rating
        filled_stars = [1] * review.rating  # Create a list with the number of filled stars
        empty_stars = [1] * (5 - review.rating)  # Create a list with the remaining empty stars
        
        if request.method == 'POST':
            review.delete()
            messages.success(request, "Your review has been deleted successfully.")
            return redirect('services:public-business-profile', vendor_id=review.vendor.id)
        else:
            # Render the confirmation page with stars data
            return render(request, 'services/confirm-delete-review.html', {
                'review': review,
                'filled_stars': filled_stars,
                'empty_stars': empty_stars,
            })
    else:
        # If the user is not the owner of the review
        messages.error(request, "You cannot delete someone else's review.")
        return redirect('services:public-business-profile', vendor_id=review.vendor.id)
    



# services/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def track_interaction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        entity_id = data.get('entity_id')

        # You can save the interaction to a model for persistence
        # Example: Interaction.objects.create(action=action, entity_id=entity_id)

        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
