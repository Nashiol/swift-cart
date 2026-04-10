from django.contrib import admin
from .models import *

#Register your models here.
admin.site.register(ProductImage)
admin.site.register(FeaturedProduct)
admin.site.register(Review)
admin.site.register(UserProductInteraction)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'vendor')
    search_fields = ('name', 'description', 'category__name')
    list_filter = ('category', 'vendor', 'status')



