from django.contrib import admin
from .models import Characteristic, Product, Category

admin.site.register(Characteristic)
admin.site.register(Product)
admin.site.register(Category)