from django import template
from core.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0

# calculate total price for items in history cart
@register.filter
def calculate_total_price(history):
    return sum(item.price * item.quantity for item in history)