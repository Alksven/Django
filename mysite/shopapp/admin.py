from django.contrib import admin

from shopapp.models import Product, Order


class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        OrderInline,
    ]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount'
    list_display_links = "pk", "name"
    ordering = "pk",
    search_fields = 'name', 'description'
    fieldsets = [
        (None, {
            "fields": ("name", "description")
        }),
        ("Price option", {
            "fields": ("price", "discount"),
            "classes": ("collapse",),
        }

        )
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '...'


class ProductInline(admin.TabularInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = 'delivery_address', 'promocode', 'created_at', 'user_verbose'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

