from django.contrib import admin
from .models import Merchant, APIKey

@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "created_at")

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ("id", "merchant", "name", "created_at", "revoked")
    readonly_fields = ("hashed_key",)
