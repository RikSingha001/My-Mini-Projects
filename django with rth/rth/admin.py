from django.contrib import admin
from .models import Order, OrderItem


# Show OrderItem inside Order (inline)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('item_name', 'price', 'quantity', 'subtotal')

    def subtotal(self, obj):
        return obj.price * obj.quantity

    subtotal.short_description = "Subtotal"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_username',
        'meal_type',
        'total_price',
        'created_at',
    )

    list_filter = ('meal_type', 'created_at')
    search_fields = ('user__username',)
    ordering = ('-created_at',)

    inlines = [OrderItemInline]

    readonly_fields = ('created_at', 'total_price')

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = "User"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item_name', 'price', 'quantity')
