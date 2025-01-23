from django.contrib import admin
from .models import Game, Developer, Category, CartItem, OrderItem, Order

# Register your models here.
admin.site.register(Game)
admin.site.register(Developer)
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Order)
