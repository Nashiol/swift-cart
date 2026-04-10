from django.contrib import admin
from.models import *

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'ordered_at')
    search_fields = ('user__email', 'id')
    list_filter = ('status', 'ordered_at')
