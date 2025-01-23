from django import template

register = template.Library()

@register.filter
def total_cart_price(cart_items):
    return sum(item.game.price for item in cart_items)