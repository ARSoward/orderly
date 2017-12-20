from django.contrib import admin

from .models import Business, Connection, Order, Product, OrderItem

admin.site.register(Business)
admin.site.register(Connection)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(OrderItem)
