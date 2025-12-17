from django.contrib import admin
from api.models import User, Product, Sell, SellItem
from django.contrib.auth.admin import UserAdmin
admin.site.register(Product)
admin.site.register(User, UserAdmin)


class SellItemInline(admin.TabularInline):
    model = SellItem


class SellAdmin(admin.ModelAdmin):
    inlines = [SellItemInline]


admin.site.register(Sell, SellAdmin)
