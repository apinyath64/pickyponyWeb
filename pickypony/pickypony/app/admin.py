from django.contrib import admin
from . models import *
from django.utils.html import format_html
from django.urls import reverse

@admin.register(Item)
class ItemModel(admin.ModelAdmin):
    list_display = ['id', 'name', 'discounted_price', 'size', 'color', 'category']

@admin.register(Customer)
class CustomerModel(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city', 'zipcode']


@admin.register(Cart)
class CartModel(admin.ModelAdmin):
    list_display = ['id', 'user', 'items', 'size', 'color', 'quantity']
    def items(self, obj):
        link = reverse("admin:app_item_change", args=[obj.item.pk])
        return format_html('<a href="{}">{}</a>', link, obj.item.name)



@admin.register(Payment)
class PaymenModel(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'charge_id', 'payment_status', 'paid']

@admin.register(OrderPlaced)
class PaymetModel(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'items', 'quantity', 'order_date', 'status', 'payment']
    def items(self, obj):
        link = reverse("admin:app_item_change", args=[obj.item.pk])
        return format_html('<a href="{}">{}</a>', link, obj.item.name)



@admin.register(Wishlist)
class WishlistModel(admin.ModelAdmin):
    list_display = ['id', 'user', 'items']
    def items(self, obj):
        link = reverse("admin:app_item_change", args=[obj.item.pk])
        return format_html('<a href="{}">{}</a>', link, obj.item.name)
