from django.contrib import admin
from.models import *

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'status', 'created_at')
    search_fields = ('customer__email', 'id')
    list_filter = ('status', 'created_at')
