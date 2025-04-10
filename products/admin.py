from django.contrib import admin
from .models import Product, ProductImage, Category

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount_price', 'category', 'date_added']
    inlines = [ProductImageInline]

# admin.site.register(Characteristic)
admin.site.register(Category)
