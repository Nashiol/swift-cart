from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Customer_Profile)
admin.site.register(Vendor_Profile)

class AccountReviewAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'review_text', 'submitted_at')  # Use user_email instead of user

admin.site.register(AccountReview, AccountReviewAdmin)
