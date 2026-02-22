from django.urls import path
from.import views

app_name = 'checkouts'

urlpatterns = [
    path('cart/', views.view_cart, name='view-cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place-order'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order-confirmation'),
    path('order/update-status/<int:order_id>/', views.update_order_status, name='update-order-status'),
    path('order/<int:order_id>/', views.order_detail, name='order-detail'),  # URL for order details  
    path('wishlist/', views.wishlist_view, name='wishlist'),  # URL for order details  
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),  # URL for order details  
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),  # URL for order details

]