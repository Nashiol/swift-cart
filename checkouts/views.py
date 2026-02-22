from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from.models import Product, Cart, CartItem, Order, OrderItem, Wishlist
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

# Create your views here.
#Adding items to cart
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Add a success message
    messages.success(request, f'{product.name} has been added to your cart.')

    return redirect('/products/')

@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart_items = []  # Empty list if the cart doesn't exist
    return render(request, 'services/cart.html', {'cart_items': cart_items})

@login_required
def remove_from_cart(request, product_id):
    # Get the current user's cart (or create one if it doesn't exist)
    cart = get_object_or_404(Cart, user=request.user)
    
    # Get the product to be removed
    product = get_object_or_404(Product, id=product_id)
    
    # Remove the item from the cart
    CartItem.objects.filter(cart=cart, product=product).delete()
    
    # Redirect back to the cart view
    return redirect('checkouts:view-cart')


@login_required
def checkout(request):
    # Get the current user's cart
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()

    # Calculate the total price
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Create an order
    order = Order.objects.create(user=request.user, total_price=total_price)

    # Link the vendor and price to each order item
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,  # Add the price explicitly
            vendor=item.product.vendor  # Assuming `vendor` is a field in the Product model
        )

    # Clear the cart
    cart.items.all().delete()

    # Render the order confirmation page
    return render(request, 'checkouts/order-confirmation.html', {'order': order})

@login_required
def place_order(request):
    # This view will handle the order placement and confirmation
    
    # Assuming cart items exist for the logged-in user
    user_cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)

    # Calculate total price
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Create an Order
    order = Order.objects.create(user=request.user, total_price=total_price)

    # Create OrderItems for each item in the cart
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price,
            vendor=cart_item.product.vendor
        )

    # Empty the cart after the order is placed
    cart_items.delete()

    # Update order status to 'Confirmed'
    order.status = 'Confirmed'
    order.save()

    # Send a confirmation email to the user
    send_order_confirmation_email(order)

    # Redirect to order confirmation page
    return redirect('order_confirmation', order_id=order.id)


def send_order_confirmation_email(order):
    subject = f"Order #{order.id} Confirmation"
    message = f"Thank you for your order!\n\nYour order #{order.id} has been confirmed. The total price is {order.total_price}.\n\nWe will notify you once your order is shipped."
    recipient_list = [order.user.email]
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'checkouts/order-confirmation.html', {'order':order})




@login_required
def update_order_status(request, order_id):
    # Get the order object by ID
    order = get_object_or_404(Order, id=order_id)
    
    # Ensure the order contains items and each item has an associated vendor
    order_items = OrderItem.objects.filter(order=order)
    if order_items.exists():
        # You can access the vendor from the first order item or iterate if needed
        vendor = order_items.first().vendor  # Example: Access vendor from the first order item
        
        if request.method == 'POST':
            new_status = request.POST.get('status')
            
            # Check if the new status is one of the valid statuses
            valid_statuses = [Order.Status.SHIPPED, Order.Status.DELIVERED, Order.Status.PENDING, Order.Status.CANCELED]
            
            if new_status in valid_statuses:
                # Handle the specific logic for "canceled" and "delivered"
                if new_status == Order.Status.CANCELED:
                    # Remove the order when canceled
                    order.delete()
                    messages.success(request, f"Order {order.id} has been canceled and removed.")
                    return redirect('services:home')  # Redirect to the order list after cancellation
                
                # Update the order status for valid statuses (excluding "canceled")
                order.status = new_status
                order.save()

                # Provide success feedback to the vendor
                messages.success(request, f"Order {order.id} status updated to {new_status}.")

                # Redirect after updating status
                return redirect('checkouts:order-detail', order_id=order_id)
            else:
                messages.error(request, "Invalid status selected.")
    else:
        messages.error(request, "This order has no items or vendors associated with it.")
    
    return render(request, 'services/vendor-order-update.html', {'order': order})



def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'checkouts/order-detail.html', {'order': order})
    

def send_order_status_update_email(order):
    subject = f"Order #{order.id} Status Updated"
    message = f"Your order #{order.id} status has been updated to {order.get_status_display()}."
    recipient_list = [order.user.email]

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'checkouts/wishlist.html', {'wishlist_items': wishlist_items})
    

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('checkouts:wishlist')  # Redirect to wishlist page


def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return redirect('checkouts:wishlist')