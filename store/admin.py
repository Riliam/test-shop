from django.contrib import admin
from store.models import Category, Product, Order, OrderDetail

class ProductInLine(admin.StackedInline):
    model = Product

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInLine]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)
