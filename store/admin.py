from django.contrib import admin
from .models import Order, Customer, OrderItem, ShippingAddress, Product

# Register your models here.

admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Product)
