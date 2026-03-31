from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(CustomUser)

class AccountReviewAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'review_text', 'submitted_at')  # Use user_email instead of user
    search_fields = ('user_email', 'review_text')

admin.site.register(AccountReview, AccountReviewAdmin)

@admin.register(Customer_Profile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'user')
    search_fields = ('name', 'email', 'phone_number', 'user__email')

@admin.register(Vendor_Profile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'user')
    search_fields = ('name', 'email', 'phone_number', 'user__email')

