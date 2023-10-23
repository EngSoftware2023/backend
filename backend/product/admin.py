from django.contrib import admin

# Register your models here.

from .models import Product

class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['name']}),
        ('Price', {'fields': ['price']}),
        ('Stock', {'fields': ['stock']}),
        ('Request', {'fields': ['request']}),
    ]
    list_display = ('name', 'price', 'stock', 'request')
    list_filter = ('name', 'price', 'stock', 'request')

admin.site.register(Product)