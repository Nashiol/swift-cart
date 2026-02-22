from django.urls import path
from .import views

app_name = 'services'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('about/', views.about_view, name = 'about'),
    path('service/', views.service, name = 'service'),
    path('contact', views.contact_page, name = 'contact'),
    path('vendor/products/', views.vendor_products, name = 'vendor-products'),
    path('vendor/products/add/', views.add_product, name = 'add-product'),
    path('vendor/products/edit/<int:pk>/', views.edit_product, name = 'edit-product'),
    path('vendor/products/delete/<int:pk>/', views.delete_product, name = 'delete-product'),
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('newsletter/', views.newsletter_signup, name='newsletter-signup'),
    path('newsletter/thanks/', views.newsletter_thanks, name='newsletter-thanks'),
    path('search/', views.search, name='search'),
    path('search/export', views.export_search_results, name='export_search_results'),
    path('vendor/<uuid:vendor_id>/products/', views.vendor_products_list, name='vendor-product-list'),
    path('public-profile/<uuid:vendor_id>/', views.public_business_profile, name='public-business-profile'),
    path('edit-review/<int:review_id>/', views.edit_review, name='edit-review'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete-review'),
    path('track-interaction', views.track_interaction, name='track-interaction'),
]