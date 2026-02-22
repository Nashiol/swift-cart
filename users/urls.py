from django.urls import path, include
from.import views

#app_name = 'users'

urlpatterns = [
    path('signup/customer/', views.customer_signup, name='customer-signup'),
    path('signup/vendor/', views.vendor_signup, name='vendor-signup'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('dashboard/vendor/', views.vendor_profile, name='vendor-profile'),
    path('customer-profile-form/', views.customerProfile, name='customer-profile-form'),
    path('vendor-profile-form/', views.vendorProfile, name='vendor-profile-form'),
    path('vendor-profile/', views.vendor_profile, name='vendor-profile'),
    path('dashboard/vendor/update', views.vendor_profile_update, name='vendor-profile-form'),
    path('customer-dashboard/', views.customer_dashboard, name='customer-dashboard'),
    path('dashboard/customer/update/', views.customer_dashboard_update, name='customer-dashboard-update'),
    path('delete/customer/', views.delete_customer_account, name='delete-customer-account'),
    path('delete/vendor/', views.delete_vendor_account, name='delete-vendor-account'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('allauth.urls')),
    path('delete-vendor-account/', views.delete_vendor_account, name='delete-vendor-account'),
    path('delete-customer-account/', views.delete_customer_account, name='delete-customer-account'),
]


